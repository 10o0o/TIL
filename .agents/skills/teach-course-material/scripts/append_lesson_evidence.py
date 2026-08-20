#!/usr/bin/env python3
"""Atomically append one confirmed learner-evidence item to til/today.md."""

from __future__ import annotations

import argparse
import os
import sys
import tempfile
from pathlib import Path


COACH_SCRIPTS = Path(__file__).resolve().parents[2] / "coach-llm-research-study" / "scripts"
if str(COACH_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(COACH_SCRIPTS))

from validate_lesson_handoff import (  # noqa: E402
    ValidationError,
    _draft_marker_blocks,
    _normalize_newlines,
    _safe_repo_path,
    validate_handoff,
)


DEFAULT_DRAFT = "<!-- 형식 없이 자유롭게 작성하세요. 저장할 때 $save-today-til을 사용합니다. -->\n"


def _atomic_write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    old_mode = path.stat().st_mode & 0o777 if path.exists() else 0o644
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    temporary = Path(temporary_name)
    try:
        os.fchmod(descriptor, old_mode)
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
        try:
            directory_fd = os.open(path.parent, os.O_RDONLY)
        except OSError:
            directory_fd = None
        if directory_fd is not None:
            try:
                os.fsync(directory_fd)
            finally:
                os.close(directory_fd)
    finally:
        if temporary.exists():
            temporary.unlink()


def _append_envelope(existing: str, envelope: str) -> str:
    if not existing:
        return envelope
    separator = "" if existing.endswith("\n\n") else "\n" if existing.endswith("\n") else "\n\n"
    return existing + separator + envelope


def _render_error(path: Path, error: ValidationError) -> str:
    return error.rendered(path)


def append_evidence(
    handoff_path: Path | str,
    evidence_id: str,
    *,
    repo_root: Path | str | None = None,
) -> tuple[int, str]:
    report = validate_handoff(handoff_path, repo_root=repo_root, check_draft=True)
    if not report.ok or report.document is None:
        return report.exit_code, "\n".join(_render_error(report.path, error) for error in report.errors)
    doc = report.document
    item = doc.evidence.get(evidence_id)
    if item is None:
        error = ValidationError(1, "EVIDENCE_STATE", f"unknown learner evidence ID: {evidence_id}")
        return 1, _render_error(report.path, error)
    if item.values.get("provenance") != "learner" or item.values.get("verdict") != "confirmed":
        error = ValidationError(item.line, "EVIDENCE_STATE", f"{evidence_id} is not confirmed learner-authored evidence")
        return 1, _render_error(report.path, error)
    if item.values.get("append_state") not in {"pending", "drafted"}:
        error = ValidationError(item.line, "EVIDENCE_STATE", f"{evidence_id} is not eligible for draft append")
        return 1, _render_error(report.path, error)
    if doc.metadata.get("status") not in {"active", "paused", "completed"}:
        error = ValidationError(item.line, "REVIEW_NOT_PASS", "evidence append requires an active, paused, or completed reviewed lesson")
        return 1, _render_error(report.path, error)

    draft_path, path_error = _safe_repo_path(doc.metadata["draft_path"], doc.repo_root)
    if path_error or draft_path is None:
        error = ValidationError(1, "PATH", f"invalid draft path: {path_error or 'unknown path error'}")
        return 1, _render_error(report.path, error)
    if draft_path.exists() and not draft_path.is_file():
        error = ValidationError(1, "PATH", "draft path is not a regular file")
        return 1, _render_error(report.path, error)
    try:
        draft_text = _normalize_newlines(draft_path.read_text(encoding="utf-8")) if draft_path.exists() else DEFAULT_DRAFT
    except UnicodeDecodeError:
        error = ValidationError(1, "DRAFT_CONTENT", "draft is not valid UTF-8")
        return 1, _render_error(report.path, error)

    lesson_id = doc.metadata["lesson_id"]
    blocks, balanced = _draft_marker_blocks(draft_text, lesson_id)
    if not balanced:
        error = ValidationError(1, "DRAFT_MARKER", "draft lesson-evidence markers are unbalanced")
        return 1, _render_error(report.path, error)
    matching = [block for block in blocks if block[0] == evidence_id]
    if len(matching) > 1:
        error = ValidationError(matching[0][3], "DRAFT_MARKER", f"duplicate draft marker for {evidence_id}")
        return 1, _render_error(report.path, error)

    content_hash = item.values["content_sha256"]
    if matching:
        _, marker_hash, marker_body, marker_line = matching[0]
        if marker_hash != content_hash or marker_body != item.content:
            error = ValidationError(marker_line, "DRAFT_CONTENT", f"existing draft envelope differs from {evidence_id}")
            return 1, _render_error(report.path, error)
        draft_changed = False
    else:
        if item.values.get("append_state") == "drafted":
            error = ValidationError(item.line, "DRAFT_MARKER", f"{evidence_id} is drafted but its marker is missing")
            return 1, _render_error(report.path, error)
        envelope = (
            f"<!-- lesson-evidence:{lesson_id}:{evidence_id}:{content_hash} -->\n"
            f"{item.content}\n"
            f"<!-- /lesson-evidence:{lesson_id}:{evidence_id} -->\n"
        )
        _atomic_write(draft_path, _append_envelope(draft_text, envelope))
        draft_changed = True

    state_changed = item.values.get("append_state") != "drafted"
    if state_changed:
        span_start, span_end = item.append_value_span
        if span_start <= 0 or span_end < span_start:
            error = ValidationError(item.line, "SCHEMA", f"cannot locate {evidence_id} append_state")
            return 2, _render_error(report.path, error)
        updated_handoff = doc.text[:span_start] + "drafted" + doc.text[span_end:]
        _atomic_write(report.path, updated_handoff)

    final_report = validate_handoff(report.path, repo_root=doc.repo_root, check_draft=True)
    if not final_report.ok:
        return final_report.exit_code, "\n".join(_render_error(final_report.path, error) for error in final_report.errors)
    if draft_changed:
        return 0, f"APPENDED {evidence_id} -> {doc.metadata['draft_path']}"
    if state_changed:
        return 0, f"RECOVERED {evidence_id} -> drafted"
    return 0, f"ALREADY_APPENDED {evidence_id}"


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("handoff", type=Path, help="repository-relative active handoff Markdown path")
    parser.add_argument("--evidence", required=True, help="learner evidence ID such as E001")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    try:
        code, message = append_evidence(args.handoff, args.evidence)
    except Exception as exc:  # pragma: no cover - last-resort CLI boundary
        print(f"ERROR {args.handoff.as_posix()}:1 [SCHEMA] internal error: {exc}", file=sys.stderr)
        return 2
    print(message, file=sys.stdout if code == 0 else sys.stderr)
    return code


if __name__ == "__main__":
    raise SystemExit(main())
