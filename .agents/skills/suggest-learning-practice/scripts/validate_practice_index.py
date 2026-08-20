#!/usr/bin/env python3
"""Validate explicit course-lesson to instructor-practice mappings in an INDEX.md."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


PRACTICE_COLUMNS = ("Practice path", "Related lesson path", "Variant", "Format", "Original")
ALLOWED_VARIANTS = {"single", "basic", "advanced"}
ALLOWED_FORMATS = {"Markdown", "PDF", "Notebook"}


@dataclass(frozen=True)
class Problem:
    line: int
    code: str
    message: str


def _cell(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == "`" and value[-1] == "`":
        return value[1:-1]
    return value


def _row(line: str) -> list[str] | None:
    stripped = line.strip()
    if not (stripped.startswith("|") and stripped.endswith("|")):
        return None
    return [part.strip() for part in stripped[1:-1].split("|")]


def _section(text: str, heading: str) -> tuple[int, list[tuple[int, str]]] | None:
    lines = text.splitlines()
    start = next((index for index, line in enumerate(lines) if line == f"## {heading}"), None)
    if start is None:
        return None
    end = next((index for index in range(start + 1, len(lines)) if lines[index].startswith("## ")), len(lines))
    return start + 1, [(index + 1, lines[index]) for index in range(start + 1, end)]


def _table(section: tuple[int, list[tuple[int, str]]], expected: tuple[str, ...]) -> tuple[list[tuple[int, list[str]]], list[Problem]]:
    _, lines = section
    problems: list[Problem] = []
    header_index = next((index for index, (_, line) in enumerate(lines) if _row(line) is not None), None)
    if header_index is None:
        return [], [Problem(lines[0][0] if lines else 1, "INDEX_SCHEMA", "table is missing")]
    header_line, header_raw = lines[header_index]
    header = _row(header_raw)
    if tuple(header or ()) != expected:
        problems.append(Problem(header_line, "INDEX_SCHEMA", f"expected columns: {' | '.join(expected)}"))
        return [], problems
    if header_index + 1 >= len(lines):
        return [], problems + [Problem(header_line, "INDEX_SCHEMA", "table separator is missing")]
    separator_line, separator_raw = lines[header_index + 1]
    separator = _row(separator_raw)
    if separator is None or len(separator) != len(expected) or not all(re.fullmatch(r":?-{3,}:?", item) for item in separator):
        problems.append(Problem(separator_line, "INDEX_SCHEMA", "table separator is invalid"))
        return [], problems
    rows: list[tuple[int, list[str]]] = []
    for line_no, raw in lines[header_index + 2 :]:
        if not raw.strip():
            continue
        parsed = _row(raw)
        if parsed is None:
            continue
        if len(parsed) != len(expected):
            problems.append(Problem(line_no, "INDEX_SCHEMA", f"row must have {len(expected)} cells"))
            continue
        rows.append((line_no, [_cell(item) for item in parsed]))
    return rows, problems


def validate(index_path: Path | str) -> list[Problem]:
    path = Path(index_path)
    if not path.is_file():
        return [Problem(1, "SOURCE_MISSING", "INDEX.md does not exist")]
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return [Problem(1, "INDEX_SCHEMA", "INDEX.md is not valid UTF-8")]

    lesson_section = _section(text, "강의 자료")
    practice_section = _section(text, "강의 제공 실습")
    problems: list[Problem] = []
    if lesson_section is None:
        problems.append(Problem(1, "INDEX_SCHEMA", "missing section: 강의 자료"))
        lesson_rows: list[tuple[int, list[str]]] = []
    else:
        # Course indexes legitimately carry two or three descriptive columns;
        # only the first path cell is part of this mapping contract.
        _, lesson_lines = lesson_section
        lesson_rows = []
        header_seen = False
        for line_no, raw in lesson_lines:
            parsed = _row(raw)
            if parsed is None:
                continue
            if not header_seen:
                header_seen = True
                continue
            if all(re.fullmatch(r":?-{3,}:?", item) for item in parsed):
                continue
            lesson_rows.append((line_no, [_cell(item) for item in parsed]))
    if practice_section is None:
        problems.append(Problem(1, "INDEX_SCHEMA", "missing section: 강의 제공 실습"))
        practice_rows: list[tuple[int, list[str]]] = []
    else:
        practice_rows, table_problems = _table(practice_section, PRACTICE_COLUMNS)
        problems.extend(table_problems)

    course_root = path.parent.resolve()
    lesson_paths = {row[0] for _, row in lesson_rows if row}
    seen_practice: set[str] = set()
    seen_mapping: set[tuple[str, str]] = set()
    listed_paths: set[str] = set()
    for line_no, row in practice_rows:
        practice_path, lesson_path, variant, format_name, original = row
        if not practice_path.startswith("course-provided-practice/"):
            problems.append(Problem(line_no, "PRACTICE_PATH", "Practice path must be under course-provided-practice/"))
        if practice_path in seen_practice:
            problems.append(Problem(line_no, "DUPLICATE", f"duplicate Practice path: {practice_path}"))
        seen_practice.add(practice_path)
        listed_paths.add(practice_path)
        if lesson_path not in lesson_paths:
            problems.append(Problem(line_no, "LESSON_LINK", f"Related lesson path is not listed under 강의 자료: {lesson_path}"))
        if variant not in ALLOWED_VARIANTS:
            problems.append(Problem(line_no, "VARIANT", f"Variant must be one of {sorted(ALLOWED_VARIANTS)}"))
        key = (lesson_path, variant)
        if key in seen_mapping:
            problems.append(Problem(line_no, "DUPLICATE", f"duplicate lesson and variant mapping: {lesson_path} / {variant}"))
        seen_mapping.add(key)
        if format_name not in ALLOWED_FORMATS:
            problems.append(Problem(line_no, "FORMAT", f"Format must be one of {sorted(ALLOWED_FORMATS)}"))
        if not original or original == "none":
            problems.append(Problem(line_no, "INDEX_SCHEMA", "Original must identify the preserved course source"))
        for label, relative in (("Practice", practice_path), ("Related lesson", lesson_path)):
            candidate = course_root / relative
            try:
                resolved = candidate.resolve(strict=False)
                resolved.relative_to(course_root)
            except (OSError, ValueError):
                problems.append(Problem(line_no, "PRACTICE_PATH", f"{label} path escapes the course directory: {relative}"))
                continue
            if not candidate.is_file():
                problems.append(Problem(line_no, "SOURCE_MISSING", f"{label} file does not exist: {relative}"))

    practice_dir = course_root / "course-provided-practice"
    actual = {
        file.relative_to(course_root).as_posix()
        for file in practice_dir.glob("*.md")
        if file.is_file()
    }
    for missing in sorted(actual - listed_paths):
        problems.append(Problem(1, "INDEX_PARITY", f"practice file is not mapped: {missing}"))
    for extra in sorted(listed_paths - actual):
        # A more precise SOURCE_MISSING is already reported on its row.
        if not (course_root / extra).is_file():
            continue
        problems.append(Problem(1, "INDEX_PARITY", f"mapped file is outside the discovered practice set: {extra}"))
    return problems


class ContractParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        self.exit(2, f"ERROR <cli>:1 [INDEX_SCHEMA] {message}\n")


def main(argv: list[str] | None = None) -> int:
    parser = ContractParser(description=__doc__)
    parser.add_argument("index", type=Path)
    args = parser.parse_args(argv)
    try:
        problems = validate(args.index)
    except Exception as exc:  # pragma: no cover
        print(f"ERROR {args.index}:1 [INDEX_SCHEMA] internal error: {exc}", file=sys.stderr)
        return 2
    for problem in problems:
        print(f"ERROR {args.index.as_posix()}:{problem.line} [{problem.code}] {problem.message}", file=sys.stderr)
    if problems:
        return 2 if any(problem.code == "INDEX_SCHEMA" for problem in problems) else 1
    print(f"OK {args.index.as_posix()} [practice-index]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
