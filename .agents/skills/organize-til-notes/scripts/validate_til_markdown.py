#!/usr/bin/env python3
"""Validate repository TIL Markdown files without third-party dependencies."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import unquote


REQUIRED_FRONTMATTER_FIELDS = (
    "title",
    "description",
    "date",
    "updated",
    "category",
    "tags",
    "publish",
)

PROHIBITED_MACRO_RE = re.compile(
    r"\\(?:operatorname|DeclareMathOperator|newcommand|renewcommand|def|require)\b"
)
INLINE_CODE_RE = re.compile(r"`[^`\n]*`")
BOLD_BEFORE_KOREAN_RE = re.compile(r"\*\*(?!\s)(?:(?!\*\*).)+?\*\*(?=[가-힣])")
PLACEHOLDER_LINES = {
    'title: "제목"',
    'description: "이 글에서 다루는 내용을 한두 문장으로 설명합니다."',
    'title: "YYYY-MM-DD 학습 기록"',
    'description: "오늘 실제로 바뀐 이해와 그 증거를 짧게 기록합니다."',
    'title: "개념 제목"',
    'description: "이 개념이 해결하는 문제와 핵심 원리를 한두 문장으로 설명합니다."',
    "date: YYYY-MM-DD",
    "updated: YYYY-MM-DD",
    "- topic",
    "- prerequisite",
    "# YYYY-MM-DD 학습 기록",
    "# 개념 제목",
    "- 자료 없이 기억한 핵심:",
    "- 이전에는:",
    "- 이제는:",
    "- 직접 해결하거나 설명한 것:",
    "- 관련 concept 또는 lab:",
    "- 남은 질문:",
    "- 다음 복습일(1·3·7·14일 중 선택):",
    "- progress 기록: `curriculum/progress.md`의 해당 항목",
    "이 개념이 없으면 무엇을 해결하기 어려운지 설명합니다.",
    "비유를 사용할 수 있지만 실제 Tensor와 연산으로 이어서 설명합니다.",
    "2~3차원 벡터, 작은 행렬, 토큰 2~3개 등으로 중간 계산을 생략하지 않습니다.",
    "각 기호와 항이 무엇을 뜻하는지 설명합니다.",
    "이 개념이 모델 학습, Transformer, 평가 또는 시스템에서 어디에 등장하는지 설명합니다.",
    "학습자가 teach-back에서 통과한 설명을 3~7문장으로 기록합니다.",
    "학습을 시작하게 된 질문이나 해결하려던 문제를 작성합니다.",
    "이 글의 결론을 먼저 작성합니다.",
    "개념의 정의와 작동 원리를 설명합니다.",
    "# 직접 실행한 최소 예제",
    "처음에는 무엇을 잘못 이해했는지 작성합니다.",
    "이 개념이 프로젝트, 머신러닝 또는 LLM 개발에서 어디에 사용되는지 작성합니다.",
    "이 글에서 반드시 기억해야 할 내용을 한 문장으로 정리합니다.",
    "- [관련 글 제목](../relative/path.md)",
    "- 자료명",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate one or more TIL Markdown files or directories."
    )
    parser.add_argument(
        "paths",
        nargs="+",
        type=Path,
        help="Markdown file or directory to validate",
    )
    return parser.parse_args()


def collect_markdown_files(paths: list[Path]) -> tuple[list[Path], list[str]]:
    files: set[Path] = set()
    errors: list[str] = []

    for path in paths:
        if not path.exists():
            errors.append(f"{path}: path does not exist")
        elif path.is_dir():
            files.update(candidate for candidate in path.rglob("*.md") if candidate.is_file())
        elif path.suffix.lower() != ".md":
            errors.append(f"{path}: expected a Markdown file")
        else:
            files.add(path)

    return sorted(files, key=lambda item: str(item)), errors


def frontmatter_end(lines: list[str]) -> int | None:
    if not lines or lines[0] != "---":
        return None
    for index in range(1, min(len(lines), 80)):
        if lines[index] == "---":
            return index
    return None


def check_frontmatter(path: Path, lines: list[str]) -> list[str]:
    errors: list[str] = []
    end = frontmatter_end(lines)
    if end is None:
        return [f"{path}: missing or unclosed YAML frontmatter"]

    keys = {
        match.group(1)
        for line in lines[1:end]
        if (match := re.match(r"^([A-Za-z][A-Za-z0-9_-]*):(?:\s|$)", line))
    }
    for field in REQUIRED_FRONTMATTER_FIELDS:
        if field not in keys:
            errors.append(f"{path}: frontmatter is missing '{field}'")

    publish_lines = [line for line in lines[1:end] if line.startswith("publish:")]
    if publish_lines and publish_lines[0] not in {"publish: true", "publish: false"}:
        errors.append(f"{path}: publish must be true or false")

    return errors


def strip_fenced_and_inline_code(lines: list[str]) -> tuple[list[tuple[int, str]], list[str]]:
    visible: list[tuple[int, str]] = []
    errors: list[str] = []
    in_fence = False
    opening_line = 0

    for line_number, line in enumerate(lines, start=1):
        if line.lstrip().startswith("```"):
            if not in_fence:
                in_fence = True
                opening_line = line_number
                marker = line.lstrip()
                if marker == "```":
                    errors.append(
                        f"line {line_number}: opening code fence needs a language identifier"
                    )
            else:
                in_fence = False
            continue
        if not in_fence:
            visible.append((line_number, INLINE_CODE_RE.sub("", line)))

    if in_fence:
        errors.append(f"line {opening_line}: unclosed fenced code block")

    return visible, errors


def check_math_and_emphasis(path: Path, visible: list[tuple[int, str]]) -> list[str]:
    errors: list[str] = []
    block_math_open = False
    block_math_line = 0

    for line_number, line in visible:
        if PROHIBITED_MACRO_RE.search(line):
            errors.append(f"{path}:{line_number}: prohibited math macro")
        if any(delimiter in line for delimiter in (r"\(", r"\)", r"\[", r"\]")):
            errors.append(
                f"{path}:{line_number}: use $...$ or $$...$$ instead of escaped delimiters"
            )
        if BOLD_BEFORE_KOREAN_RE.search(line):
            errors.append(
                f"{path}:{line_number}: Korean text follows a closing bold marker directly"
            )

        index = 0
        inline_dollars = 0
        while index < len(line):
            if line.startswith("$$", index) and (index == 0 or line[index - 1] != "\\"):
                if not block_math_open:
                    block_math_line = line_number
                block_math_open = not block_math_open
                index += 2
                continue
            if (
                line[index] == "$"
                and (index == 0 or line[index - 1] != "\\")
                and not block_math_open
            ):
                inline_dollars += 1
            index += 1

        if inline_dollars % 2:
            errors.append(f"{path}:{line_number}: unbalanced inline math delimiter")

    if block_math_open:
        errors.append(f"{path}:{block_math_line}: unclosed block math delimiter")

    return errors


def normalize_link_target(raw_target: str) -> str:
    target = raw_target.strip()
    if target.startswith("<") and ">" in target:
        target = target[1 : target.index(">")]
    elif " " in target:
        target = target.split(maxsplit=1)[0]
    return unquote(target.split("#", maxsplit=1)[0])


def extract_link_targets(line: str) -> list[str]:
    """Extract Markdown link targets while allowing balanced parentheses."""
    targets: list[str] = []
    cursor = 0

    while True:
        start = line.find("](", cursor)
        if start == -1:
            return targets

        index = start + 2
        depth = 1
        escaped = False
        while index < len(line):
            character = line[index]
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif character == "(":
                depth += 1
            elif character == ")":
                depth -= 1
                if depth == 0:
                    targets.append(line[start + 2 : index])
                    cursor = index + 1
                    break
            index += 1
        else:
            return targets


def check_links(path: Path, visible: list[tuple[int, str]]) -> list[str]:
    errors: list[str] = []
    for line_number, line in visible:
        for raw_target in extract_link_targets(line):
            target = normalize_link_target(raw_target)
            if not target or target.startswith(("#", "http://", "https://", "mailto:", "data:")):
                continue
            destination = (path.parent / target).resolve()
            if not destination.exists():
                errors.append(
                    f"{path}:{line_number}: relative link target does not exist: {target}"
                )
    return errors


def validate_file(path: Path) -> list[str]:
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return [f"{path}: file is not valid UTF-8"]

    lines = text.splitlines()
    errors: list[str] = []
    if not text.endswith("\n"):
        errors.append(f"{path}: missing final newline")

    errors.extend(check_frontmatter(path, lines))
    visible, fence_errors = strip_fenced_and_inline_code(lines)
    errors.extend(f"{path}:{message}" for message in fence_errors)
    errors.extend(check_math_and_emphasis(path, visible))
    errors.extend(check_links(path, visible))

    frontmatter_boundary = frontmatter_end(lines)
    body_start = (frontmatter_boundary + 1) if frontmatter_boundary is not None else 0
    top_headings = [
        line_number
        for line_number, line in visible
        if line_number > body_start and re.match(r"^#\s+\S", line)
    ]
    if len(top_headings) != 1:
        errors.append(f"{path}: expected exactly one top-level heading, found {len(top_headings)}")

    for line_number, line in visible:
        if line.strip() in PLACEHOLDER_LINES:
            errors.append(f"{path}:{line_number}: template placeholder remains")

    return errors


def main() -> int:
    args = parse_args()
    files, errors = collect_markdown_files(args.paths)
    if not files and not errors:
        errors.append("no Markdown files found")

    for path in files:
        file_errors = validate_file(path)
        if "templates" in path.parts:
            file_errors = [
                error for error in file_errors if "template placeholder remains" not in error
            ]
        errors.extend(file_errors)

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"Validation failed with {len(errors)} error(s).", file=sys.stderr)
        return 1

    print(f"Validated {len(files)} Markdown file(s): OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
