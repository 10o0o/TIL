#!/usr/bin/env python3
"""Validate the ignored active-lesson handoff and its source/draft state."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import dataclass, field
from datetime import date, datetime
from pathlib import Path, PurePosixPath
from typing import Any


STATUSES = {"preparing", "review_pending", "active", "paused", "blocked", "completed"}
MANIFEST_ROLES = {
    "primary",
    "asset",
    "course-index",
    "curriculum",
    "knowledge",
    "til",
    "practice",
}
REVIEW_VERDICTS = {"pending", "pass", "changes_required", "unavailable"}
EVIDENCE_KINDS = {
    "explain_back",
    "calculation",
    "shape_prediction",
    "code_interpretation",
    "transfer",
    "limit",
}
EVIDENCE_VERDICTS = {"confirmed", "partial", "misconception", "unconfirmed"}
APPEND_STATES = {"pending", "drafted", "not_eligible"}
CONCEPT_MARKERS = {"none", "[선수개념]", "[정정]", "[보충]"}
HASH_RE = re.compile(r"[0-9a-f]{64}\Z")
LESSON_ID_RE = re.compile(r"[a-z0-9][a-z0-9-]{2,63}\Z")
AGENT_ID_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9._/@-]{1,127}\Z")
CURRICULUM_ID_RE = re.compile(r"(?:CC|TR)-[A-Z]+-\d{2}\Z")

METADATA_KEYS = (
    "schema_version",
    "lesson_id",
    "title",
    "status",
    "study_date",
    "created_at",
    "updated_at",
    "author_id",
    "draft_path",
    "input_manifest_sha256",
    "contract_sha256",
)
CURRENT_POSITION_KEYS = ("last_completed", "next_concept", "next_question")
REVIEW_KEYS = (
    "reviewer_id",
    "reviewer_mode",
    "reviewed_at",
    "verdict",
    "reviewed_input_manifest_sha256",
    "reviewed_contract_sha256",
)
EVIDENCE_KEYS = (
    "concept",
    "kind",
    "provenance",
    "verdict",
    "append_state",
    "captured_at",
    "content_sha256",
)
CONTRACT_HEADINGS = (
    "Objective",
    "Curriculum Targets",
    "Learner Evidence Baseline",
    "Corrections, Prerequisites, and Supplements",
    "Concept Path",
    "Prepared Teaching Notes",
    "Deferred",
)


@dataclass
class ValidationError:
    line: int
    code: str
    message: str

    def rendered(self, path: Path) -> str:
        return f"ERROR {path.as_posix()}:{self.line} [{self.code}] {self.message}"

    def as_json(self) -> dict[str, Any]:
        return {"line": self.line, "code": self.code, "message": self.message}


@dataclass
class ManifestEntry:
    item_id: str
    role: str
    path: str
    sha256: str
    line: int


@dataclass
class ReviewAttempt:
    attempt: int
    values: dict[str, str]
    line: int


@dataclass
class Evidence:
    evidence_id: str
    values: dict[str, str]
    content: str
    assessment: str
    line: int
    append_value_span: tuple[int, int]


@dataclass
class HandoffDocument:
    path: Path
    repo_root: Path
    text: str
    metadata: dict[str, str] = field(default_factory=dict)
    manifest: list[ManifestEntry] = field(default_factory=list)
    contract: str = ""
    contract_concepts: list[str] = field(default_factory=list)
    curriculum_targets: list[str] = field(default_factory=list)
    review_attempt_count: int | None = None
    reviews: list[ReviewAttempt] = field(default_factory=list)
    current_position: dict[str, str] = field(default_factory=dict)
    evidence: dict[str, Evidence] = field(default_factory=dict)
    computed_manifest_sha256: str = ""
    computed_contract_sha256: str = ""


@dataclass
class ValidationReport:
    path: Path
    ready_requested: bool
    errors: list[ValidationError]
    document: HandoffDocument | None

    @property
    def ok(self) -> bool:
        return not self.errors

    @property
    def exit_code(self) -> int:
        if not self.errors:
            return 0
        return 2 if any(error.code == "SCHEMA" for error in self.errors) else 1

    def as_json(self) -> dict[str, Any]:
        computed: dict[str, str] = {}
        if self.document is not None:
            computed = {
                "input_manifest_sha256": self.document.computed_manifest_sha256,
                "contract_sha256": self.document.computed_contract_sha256,
            }
        return {
            "ok": self.ok,
            "path": self.path.as_posix(),
            "ready": self.ready_requested and self.ok,
            "computed": computed,
            "errors": [error.as_json() for error in self.errors],
        }


def _normalize_newlines(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def _repo_root_from_script() -> Path:
    script = Path(__file__).resolve()
    for candidate in script.parents:
        if (candidate / ".git").exists() or (candidate / "AGENTS.md").is_file():
            return candidate.resolve()
    raise RuntimeError("could not locate repository root")


def _is_rfc3339(value: str) -> bool:
    try:
        parsed = datetime.fromisoformat(value[:-1] + "+00:00" if value.endswith("Z") else value)
    except ValueError:
        return False
    return parsed.tzinfo is not None


def _is_date(value: str) -> bool:
    try:
        date.fromisoformat(value)
    except ValueError:
        return False
    return bool(re.fullmatch(r"\d{4}-\d{2}-\d{2}", value))


def _section_ranges(text: str, errors: list[ValidationError]) -> dict[str, tuple[int, int, int]]:
    expected = (
        "Metadata",
        "Input Manifest",
        "Semantic Review",
        "Current Position",
        "Learner Evidence",
    )
    headings = list(re.finditer(r"^## ([^\n]+)$", text, re.MULTILINE))
    found = [match.group(1) for match in headings]
    if found != list(expected):
        errors.append(
            ValidationError(
                1,
                "SCHEMA",
                "level-two headings must appear exactly once in this order: " + ", ".join(expected),
            )
        )
    ranges: dict[str, tuple[int, int, int]] = {}
    for index, match in enumerate(headings):
        name = match.group(1)
        if name not in expected or name in ranges:
            continue
        body_start = match.end()
        if text[body_start : body_start + 1] == "\n":
            body_start += 1
        body_end = headings[index + 1].start() if index + 1 < len(headings) else len(text)
        ranges[name] = (body_start, body_end, _line_number(text, match.start()))
    return ranges


def _parse_bullets(
    text: str,
    start: int,
    end: int,
    expected_keys: tuple[str, ...],
    errors: list[ValidationError],
    *,
    context: str,
) -> tuple[dict[str, str], dict[str, int], dict[str, tuple[int, int]]]:
    values: dict[str, str] = {}
    lines: dict[str, int] = {}
    spans: dict[str, tuple[int, int]] = {}
    region = text[start:end]
    for match in re.finditer(r"^- ([a-z0-9_]+):[ \t]*(.*)$", region, re.MULTILINE):
        key, value = match.group(1), match.group(2).strip()
        absolute = start + match.start()
        if key in values:
            errors.append(ValidationError(_line_number(text, absolute), "SCHEMA", f"duplicate {context} field: {key}"))
            continue
        values[key] = value
        lines[key] = _line_number(text, absolute)
        spans[key] = (start + match.start(2), start + match.end(2))
    missing = [key for key in expected_keys if key not in values]
    extra = [key for key in values if key not in expected_keys]
    if missing:
        errors.append(ValidationError(_line_number(text, start), "SCHEMA", f"missing {context} fields: {', '.join(missing)}"))
    if extra:
        errors.append(ValidationError(lines[extra[0]], "SCHEMA", f"unknown {context} fields: {', '.join(extra)}"))
    return values, lines, spans


def _safe_repo_path(raw: str, repo_root: Path) -> tuple[Path | None, str | None]:
    if not raw or raw.startswith("/") or "\\" in raw:
        return None, "path must be a non-empty POSIX repository-relative path"
    components = raw.split("/")
    if any(component in {"", ".", ".."} for component in components):
        return None, "path must not contain empty, '.' or '..' components"
    pure = PurePosixPath(raw)
    if pure.is_absolute() or pure.as_posix() != raw:
        return None, "path is not canonical POSIX repository-relative syntax"
    candidate = repo_root.joinpath(*pure.parts)
    try:
        resolved = candidate.resolve(strict=False)
        resolved.relative_to(repo_root.resolve())
    except (OSError, ValueError):
        return None, "path or symlink escapes the repository"
    return candidate, None


def _marker_body(
    text: str,
    start_marker: str,
    end_marker: str,
    errors: list[ValidationError],
    *,
    code: str = "SCHEMA",
) -> tuple[str, int, int] | None:
    start_matches = list(re.finditer(rf"^{re.escape(start_marker)}[ \t]*$", text, re.MULTILINE))
    end_matches = list(re.finditer(rf"^{re.escape(end_marker)}[ \t]*$", text, re.MULTILINE))
    if len(start_matches) != 1 or len(end_matches) != 1:
        errors.append(
            ValidationError(
                1,
                code,
                f"expected exactly one marker pair: {start_marker} ... {end_marker}",
            )
        )
        return None
    start_match, end_match = start_matches[0], end_matches[0]
    if start_match.end() >= end_match.start():
        errors.append(ValidationError(_line_number(text, start_match.start()), code, "marker order is invalid"))
        return None
    body_start = start_match.end()
    if text[body_start : body_start + 1] == "\n":
        body_start += 1
    body_end = end_match.start()
    if body_end > body_start and text[body_end - 1 : body_end] == "\n":
        body_end -= 1
    return text[body_start:body_end], body_start, body_end


def _parse_metadata(
    doc: HandoffDocument,
    section: tuple[int, int, int] | None,
    errors: list[ValidationError],
) -> dict[str, int]:
    if section is None:
        return {}
    start, end, _ = section
    values, lines, _ = _parse_bullets(text=doc.text, start=start, end=end, expected_keys=METADATA_KEYS, errors=errors, context="metadata")
    doc.metadata = values
    if values.get("schema_version") != "1":
        errors.append(ValidationError(lines.get("schema_version", 1), "SCHEMA", "schema_version must be 1"))
    if "lesson_id" in values and not LESSON_ID_RE.fullmatch(values["lesson_id"]):
        errors.append(ValidationError(lines["lesson_id"], "SCHEMA", "lesson_id has an invalid format"))
    if not values.get("title"):
        errors.append(ValidationError(lines.get("title", 1), "SCHEMA", "title must not be empty"))
    if values.get("status") not in STATUSES:
        errors.append(ValidationError(lines.get("status", 1), "SCHEMA", "status is not allowed"))
    if "study_date" in values and not _is_date(values["study_date"]):
        errors.append(ValidationError(lines["study_date"], "SCHEMA", "study_date must be YYYY-MM-DD"))
    for key in ("created_at", "updated_at"):
        if key in values and not _is_rfc3339(values[key]):
            errors.append(ValidationError(lines[key], "SCHEMA", f"{key} must be an RFC 3339 timestamp with a timezone"))
    if "author_id" in values and not AGENT_ID_RE.fullmatch(values["author_id"]):
        errors.append(ValidationError(lines["author_id"], "SCHEMA", "author_id has an invalid format"))
    if values.get("draft_path") != "til/today.md":
        errors.append(ValidationError(lines.get("draft_path", 1), "PATH", "draft_path must be til/today.md"))
    for key in ("input_manifest_sha256", "contract_sha256"):
        if key in values and not HASH_RE.fullmatch(values[key]):
            errors.append(ValidationError(lines[key], "SCHEMA", f"{key} must be 64 lowercase hexadecimal characters"))
    return lines


def _split_table_row(line: str) -> list[str] | None:
    stripped = line.strip()
    if not stripped.startswith("|") or not stripped.endswith("|"):
        return None
    return [cell.strip() for cell in stripped[1:-1].split("|")]


def _parse_manifest(
    doc: HandoffDocument,
    section: tuple[int, int, int] | None,
    errors: list[ValidationError],
) -> None:
    if section is None:
        return
    start, end, _ = section
    contract_marker = doc.text.find("<!-- lesson-contract:start -->", start, end)
    if contract_marker != -1:
        end = contract_marker
    lines_with_ends = doc.text[start:end].splitlines(keepends=True)
    offsets: list[int] = []
    cursor = start
    for line in lines_with_ends:
        offsets.append(cursor)
        cursor += len(line)
    nonblank = [(index, line.rstrip("\n")) for index, line in enumerate(lines_with_ends) if line.strip()]
    if len(nonblank) < 3:
        errors.append(ValidationError(_line_number(doc.text, start), "SCHEMA", "Input Manifest must contain a header, separator, and rows"))
        return
    header = _split_table_row(nonblank[0][1])
    separator = _split_table_row(nonblank[1][1])
    if header != ["ID", "Role", "Path", "SHA-256"]:
        errors.append(ValidationError(_line_number(doc.text, offsets[nonblank[0][0]]), "SCHEMA", "Input Manifest columns must be ID | Role | Path | SHA-256"))
    if separator is None or len(separator) != 4 or not all(re.fullmatch(r":?-{3,}:?", cell) for cell in separator):
        errors.append(ValidationError(_line_number(doc.text, offsets[nonblank[1][0]]), "SCHEMA", "Input Manifest separator is invalid"))
    entries: list[ManifestEntry] = []
    for row_number, (line_index, line) in enumerate(nonblank[2:], start=1):
        row = _split_table_row(line)
        absolute = offsets[line_index]
        line_no = _line_number(doc.text, absolute)
        if row is None or len(row) != 4:
            errors.append(ValidationError(line_no, "SCHEMA", "manifest row must have four cells"))
            continue
        item_id, role, raw_path, sha256 = row
        expected_id = f"I{row_number:03d}"
        if item_id != expected_id:
            errors.append(ValidationError(line_no, "SCHEMA", f"manifest ID must be {expected_id}"))
        if role not in MANIFEST_ROLES:
            errors.append(ValidationError(line_no, "SCHEMA", f"unknown manifest role: {role}"))
        if not HASH_RE.fullmatch(sha256):
            errors.append(ValidationError(line_no, "SCHEMA", "manifest SHA-256 must be 64 lowercase hexadecimal characters"))
        entries.append(ManifestEntry(item_id, role, raw_path, sha256, line_no))
    doc.manifest = entries

    paths = [entry.path for entry in entries]
    duplicate_paths = sorted({path for path in paths if paths.count(path) > 1})
    if duplicate_paths:
        errors.append(ValidationError(entries[0].line if entries else 1, "PATH", "duplicate manifest paths: " + ", ".join(duplicate_paths)))
    if not any(entry.role == "primary" for entry in entries):
        errors.append(ValidationError(_line_number(doc.text, start), "SCHEMA", "manifest requires at least one primary input"))
    if sum(entry.role == "curriculum" for entry in entries) != 1:
        errors.append(ValidationError(_line_number(doc.text, start), "SCHEMA", "manifest requires exactly one curriculum input"))
    for entry in entries:
        if entry.role == "curriculum" and entry.path != "CURRICULUM.md":
            errors.append(ValidationError(entry.line, "PATH", "the curriculum manifest path must be exactly CURRICULUM.md"))
        if entry.path == doc.metadata.get("draft_path"):
            errors.append(ValidationError(entry.line, "PATH", "the mutable draft_path must not be included in the Input Manifest"))

    canonical_rows: list[str] = []
    for entry in entries:
        candidate, path_error = _safe_repo_path(entry.path, doc.repo_root)
        if path_error:
            errors.append(ValidationError(entry.line, "PATH", path_error))
            continue
        assert candidate is not None
        if not candidate.exists() or not candidate.is_file():
            errors.append(ValidationError(entry.line, "SOURCE_MISSING", f"manifest file does not exist: {entry.path}"))
            continue
        actual_hash = _sha256_bytes(candidate.read_bytes())
        if HASH_RE.fullmatch(entry.sha256) and actual_hash != entry.sha256:
            errors.append(ValidationError(entry.line, "SOURCE_HASH", f"hash mismatch for {entry.path}: expected {entry.sha256}, got {actual_hash}"))
        canonical_rows.append(f"{entry.role}\t{entry.path}\t{entry.sha256}\n")
    all_rows = [f"{entry.role}\t{entry.path}\t{entry.sha256}\n" for entry in entries]
    doc.computed_manifest_sha256 = _sha256_bytes("".join(sorted(all_rows)).encode("utf-8"))


def _contract_sections(contract: str) -> tuple[dict[str, str], list[tuple[str, int]]]:
    matches = list(re.finditer(r"^### ([^\n]+)$", contract, re.MULTILINE))
    sections: dict[str, str] = {}
    headings: list[tuple[str, int]] = []
    for index, match in enumerate(matches):
        name = match.group(1)
        body_start = match.end()
        if contract[body_start : body_start + 1] == "\n":
            body_start += 1
        body_end = matches[index + 1].start() if index + 1 < len(matches) else len(contract)
        sections[name] = contract[body_start:body_end].strip("\n")
        headings.append((name, match.start()))
    return sections, headings


def _parse_contract(doc: HandoffDocument, errors: list[ValidationError]) -> None:
    marked = _marker_body(doc.text, "<!-- lesson-contract:start -->", "<!-- lesson-contract:end -->", errors)
    if marked is None:
        return
    contract, body_start, _ = marked
    doc.contract = contract
    doc.computed_contract_sha256 = _sha256_bytes(contract.encode("utf-8"))
    sections, headings = _contract_sections(contract)
    if [name for name, _ in headings] != list(CONTRACT_HEADINGS):
        errors.append(ValidationError(_line_number(doc.text, body_start), "SCHEMA", "Lesson Contract headings are missing, duplicated, extra, or out of order"))
        return
    for heading in CONTRACT_HEADINGS:
        if not sections.get(heading, "").strip():
            relative_line = next((offset for name, offset in headings if name == heading), 0)
            errors.append(ValidationError(_line_number(doc.text, body_start + relative_line), "SCHEMA", f"contract section must not be empty: {heading}"))

    target_lines = [line.strip()[2:].strip() for line in sections["Curriculum Targets"].splitlines() if line.strip().startswith("- ")]
    if not 1 <= len(target_lines) <= 3 or len(target_lines) != len(set(target_lines)):
        errors.append(ValidationError(_line_number(doc.text, body_start), "SCHEMA", "Curriculum Targets must contain one to three unique IDs"))
    for target in target_lines:
        if not CURRICULUM_ID_RE.fullmatch(target):
            errors.append(ValidationError(_line_number(doc.text, body_start), "SCHEMA", f"invalid curriculum target ID: {target}"))
    doc.curriculum_targets = target_lines

    concept_rows: list[tuple[int, str, str, str, str]] = []
    for line in sections["Concept Path"].splitlines():
        if not line.strip():
            continue
        match = re.fullmatch(r"(\d+)\. (C\d{2}) \| (none|\[선수개념\]|\[정정\]|\[보충\]) \| (.+?) \| source: (.+)", line.strip())
        if match is None:
            errors.append(ValidationError(_line_number(doc.text, body_start), "SCHEMA", f"invalid Concept Path row: {line.strip()}"))
            continue
        ordinal, concept_id, marker, name, location = match.groups()
        concept_rows.append((int(ordinal), concept_id, marker, name.strip(), location.strip()))
    if not 3 <= len(concept_rows) <= 7:
        errors.append(ValidationError(_line_number(doc.text, body_start), "SCHEMA", "Concept Path must contain three to seven concepts"))
    for index, (ordinal, concept_id, marker, name, location) in enumerate(concept_rows, start=1):
        if ordinal != index or concept_id != f"C{index:02d}":
            errors.append(ValidationError(_line_number(doc.text, body_start), "SCHEMA", "Concept Path ordinals and IDs must be contiguous"))
        if marker not in CONCEPT_MARKERS or not name:
            errors.append(ValidationError(_line_number(doc.text, body_start), "SCHEMA", f"invalid Concept Path entry: {concept_id}"))
        if "#" not in location or not location.rsplit("#", 1)[1].strip():
            errors.append(ValidationError(_line_number(doc.text, body_start), "SCHEMA", f"{concept_id} source must include an exact #location"))
        else:
            location_path = location.rsplit("#", 1)[0]
            manifest_paths = {entry.path for entry in doc.manifest}
            if location_path not in manifest_paths:
                errors.append(
                    ValidationError(
                        _line_number(doc.text, body_start),
                        "REVIEW_NOT_PASS",
                        f"{concept_id} source path is not in the Input Manifest: {location_path}",
                    )
                )
    doc.contract_concepts = [row[1] for row in concept_rows]

    curriculum_entry = next((entry for entry in doc.manifest if entry.role == "curriculum" and entry.path == "CURRICULUM.md"), None)
    if curriculum_entry is not None:
        curriculum_path, path_error = _safe_repo_path(curriculum_entry.path, doc.repo_root)
        if path_error is None and curriculum_path is not None and curriculum_path.is_file():
            try:
                curriculum_text = curriculum_path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                errors.append(ValidationError(curriculum_entry.line, "SCHEMA", "CURRICULUM.md is not valid UTF-8"))
            else:
                for target in target_lines:
                    if CURRICULUM_ID_RE.fullmatch(target) and re.search(
                        rf"(?<![A-Z0-9-]){re.escape(target)}(?![A-Z0-9-])", curriculum_text
                    ) is None:
                        errors.append(
                            ValidationError(
                                _line_number(doc.text, body_start),
                                "REVIEW_NOT_PASS",
                                f"Curriculum Target is absent from CURRICULUM.md: {target}",
                            )
                        )

    notes = sections["Prepared Teaching Notes"]
    note_matches = list(re.finditer(r"^#### (C\d{2})$", notes, re.MULTILINE))
    note_ids = [match.group(1) for match in note_matches]
    if note_ids != doc.contract_concepts:
        errors.append(ValidationError(_line_number(doc.text, body_start), "SCHEMA", "Prepared Teaching Notes must contain one ordered subsection per concept"))
    for index, match in enumerate(note_matches):
        note_start = match.end()
        note_end = note_matches[index + 1].start() if index + 1 < len(note_matches) else len(notes)
        note_body = notes[note_start:note_end]
        fields = dict(re.findall(r"^- (tiny_example|check_question):[ \t]*(.+)$", note_body, re.MULTILINE))
        if set(fields) != {"tiny_example", "check_question"} or not all(value.strip() for value in fields.values()):
            errors.append(ValidationError(_line_number(doc.text, body_start), "SCHEMA", f"{match.group(1)} requires non-empty tiny_example and check_question fields"))


def _parse_review_attempts(
    doc: HandoffDocument,
    section: tuple[int, int, int] | None,
    errors: list[ValidationError],
) -> None:
    if section is None:
        return
    start, end, _ = section
    region = doc.text[start:end]
    top_match = re.search(r"^- review_attempt:[ \t]*(\S+)[ \t]*$", region, re.MULTILINE)
    if top_match is None:
        errors.append(ValidationError(_line_number(doc.text, start), "SCHEMA", "Semantic Review requires review_attempt"))
    else:
        try:
            doc.review_attempt_count = int(top_match.group(1))
        except ValueError:
            errors.append(ValidationError(_line_number(doc.text, start + top_match.start()), "SCHEMA", "review_attempt must be 0, 1, or 2"))

    start_matches = list(re.finditer(r"^<!-- semantic-review-attempt:(\d+):start -->[ \t]*$", region, re.MULTILINE))
    end_matches = list(re.finditer(r"^<!-- semantic-review-attempt:(\d+):end -->[ \t]*$", region, re.MULTILINE))
    if len(start_matches) != len(end_matches):
        errors.append(ValidationError(_line_number(doc.text, start), "SCHEMA", "semantic-review attempt markers are unbalanced"))
        return
    attempts: list[ReviewAttempt] = []
    for index, start_match in enumerate(start_matches):
        attempt = int(start_match.group(1))
        end_match = next((candidate for candidate in end_matches if int(candidate.group(1)) == attempt and candidate.start() > start_match.end()), None)
        if end_match is None:
            errors.append(ValidationError(_line_number(doc.text, start + start_match.start()), "SCHEMA", f"missing end marker for review attempt {attempt}"))
            continue
        body_start = start + start_match.end()
        if doc.text[body_start : body_start + 1] == "\n":
            body_start += 1
        body_end = start + end_match.start()
        body = doc.text[body_start:body_end]
        heading = re.search(rf"^### Review Attempt {attempt}$", body, re.MULTILINE)
        findings = re.search(r"^#### Blocking Findings$", body, re.MULTILINE)
        if heading is None or findings is None or heading.start() > findings.start():
            errors.append(ValidationError(_line_number(doc.text, body_start), "SCHEMA", f"review attempt {attempt} structure is invalid"))
            continue
        values_start = body_start + heading.end()
        values_end = body_start + findings.start()
        values, lines, _ = _parse_bullets(doc.text, values_start, values_end, REVIEW_KEYS, errors, context=f"review attempt {attempt}")
        findings_start = body_start + findings.end()
        if not doc.text[findings_start:body_end].strip():
            errors.append(ValidationError(_line_number(doc.text, findings_start), "SCHEMA", f"review attempt {attempt} Blocking Findings must not be empty"))
        if values.get("reviewer_mode") != "fresh-subagent":
            errors.append(ValidationError(lines.get("reviewer_mode", _line_number(doc.text, body_start)), "REVIEW_NOT_PASS", "reviewer_mode must be fresh-subagent"))
        if "reviewer_id" in values and not AGENT_ID_RE.fullmatch(values["reviewer_id"]):
            errors.append(ValidationError(lines["reviewer_id"], "SCHEMA", "reviewer_id has an invalid format"))
        if "reviewed_at" in values and not _is_rfc3339(values["reviewed_at"]):
            errors.append(ValidationError(lines["reviewed_at"], "SCHEMA", "reviewed_at must be an RFC 3339 timestamp with a timezone"))
        if values.get("verdict") not in REVIEW_VERDICTS:
            errors.append(ValidationError(lines.get("verdict", _line_number(doc.text, body_start)), "SCHEMA", "review verdict is not allowed"))
        for key in ("reviewed_input_manifest_sha256", "reviewed_contract_sha256"):
            if key in values and not HASH_RE.fullmatch(values[key]):
                errors.append(ValidationError(lines[key], "SCHEMA", f"{key} must be 64 lowercase hexadecimal characters"))
        attempts.append(ReviewAttempt(attempt, values, _line_number(doc.text, start + start_match.start())))

    attempts.sort(key=lambda item: item.attempt)
    doc.reviews = attempts
    expected_numbers = list(range(1, len(attempts) + 1))
    if [item.attempt for item in attempts] != expected_numbers:
        errors.append(ValidationError(_line_number(doc.text, start), "SCHEMA", "review attempt IDs must be contiguous from 1"))
    if len(attempts) > 2 or doc.review_attempt_count not in {0, 1, 2}:
        errors.append(ValidationError(_line_number(doc.text, start), "SCHEMA", "review_attempt is limited to 2"))
    if doc.review_attempt_count is not None and doc.review_attempt_count != len(attempts):
        errors.append(ValidationError(_line_number(doc.text, start), "SCHEMA", "review_attempt must equal the number of attempt blocks"))

    author_id = doc.metadata.get("author_id")
    reviewer_ids = [attempt.values.get("reviewer_id", "") for attempt in attempts]
    for attempt, reviewer_id in zip(attempts, reviewer_ids):
        if reviewer_id and reviewer_id == author_id:
            errors.append(ValidationError(attempt.line, "REVIEW_NOT_PASS", "fresh reviewer must differ from contract author"))
    if len(reviewer_ids) != len(set(reviewer_ids)):
        errors.append(ValidationError(attempts[-1].line if attempts else 1, "REVIEW_NOT_PASS", "each semantic review attempt requires a different fresh reviewer"))
    if len(attempts) == 2 and attempts[0].values.get("verdict") != "changes_required":
        errors.append(ValidationError(attempts[1].line, "REVIEW_NOT_PASS", "a second review is allowed only after changes_required"))

    status = doc.metadata.get("status")
    if status == "preparing" and attempts:
        errors.append(ValidationError(attempts[0].line, "REVIEW_NOT_PASS", "preparing status cannot contain review attempts"))
    if attempts:
        latest = attempts[-1]
        verdict = latest.values.get("verdict")
        if verdict == "unavailable" and status != "blocked":
            errors.append(ValidationError(latest.line, "REVIEW_NOT_PASS", "unavailable reviewer requires blocked status"))
        if latest.attempt == 2 and verdict != "pass" and status != "blocked":
            errors.append(ValidationError(latest.line, "REVIEW_NOT_PASS", "a second non-pass review requires blocked status"))
        reviewed_manifest = latest.values.get("reviewed_input_manifest_sha256")
        reviewed_contract = latest.values.get("reviewed_contract_sha256")
        if verdict == "pass" and (
            reviewed_manifest != doc.computed_manifest_sha256
            or reviewed_contract != doc.computed_contract_sha256
        ):
            errors.append(ValidationError(latest.line, "REVIEW_STALE", "pass verdict hashes do not match the current manifest and contract"))
        if verdict == "pass" and any(
            error.code in {"SOURCE_MISSING", "SOURCE_HASH", "PATH"} for error in errors
        ):
            errors.append(ValidationError(latest.line, "REVIEW_STALE", "pass verdict is stale because a manifested input is unavailable or changed"))
    if status in {"active", "paused", "completed"}:
        if not attempts or attempts[-1].values.get("verdict") != "pass":
            errors.append(ValidationError(_line_number(doc.text, start), "REVIEW_NOT_PASS", f"{status} status requires a latest pass verdict"))


def _parse_current_position(
    doc: HandoffDocument,
    section: tuple[int, int, int] | None,
    errors: list[ValidationError],
) -> None:
    if section is None:
        return
    start, end, _ = section
    values, lines, _ = _parse_bullets(doc.text, start, end, CURRENT_POSITION_KEYS, errors, context="Current Position")
    doc.current_position = values
    for key in CURRENT_POSITION_KEYS:
        if key in values and not values[key]:
            errors.append(ValidationError(lines[key], "SCHEMA", f"{key} must not be empty"))
    next_concept = values.get("next_concept")
    last_completed = values.get("last_completed")
    status = doc.metadata.get("status")
    if last_completed and last_completed != "none" and last_completed not in doc.contract_concepts:
        errors.append(ValidationError(lines.get("last_completed", 1), "SCHEMA", "last_completed must be a contract concept ID or none"))
    if next_concept and next_concept != "none" and next_concept not in doc.contract_concepts:
        errors.append(ValidationError(lines.get("next_concept", 1), "SCHEMA", "next_concept must be a contract concept ID or none"))
    if status != "completed" and next_concept == "none":
        errors.append(ValidationError(lines.get("next_concept", 1), "SCHEMA", "only a completed lesson may have next_concept: none"))


def _parse_evidence(
    doc: HandoffDocument,
    section: tuple[int, int, int] | None,
    errors: list[ValidationError],
) -> None:
    if section is None:
        return
    start, end, _ = section
    region = doc.text[start:end]
    start_matches = list(re.finditer(r"^<!-- learner-evidence:(E\d{3}):start -->[ \t]*$", region, re.MULTILINE))
    end_matches = list(re.finditer(r"^<!-- learner-evidence:(E\d{3}):end -->[ \t]*$", region, re.MULTILINE))
    if len(start_matches) != len(end_matches):
        errors.append(ValidationError(_line_number(doc.text, start), "SCHEMA", "learner-evidence markers are unbalanced"))
        return
    evidence_items: list[Evidence] = []
    for start_match in start_matches:
        evidence_id = start_match.group(1)
        end_match = next((candidate for candidate in end_matches if candidate.group(1) == evidence_id and candidate.start() > start_match.end()), None)
        if end_match is None:
            errors.append(ValidationError(_line_number(doc.text, start + start_match.start()), "SCHEMA", f"missing end marker for {evidence_id}"))
            continue
        body_start = start + start_match.end()
        if doc.text[body_start : body_start + 1] == "\n":
            body_start += 1
        body_end = start + end_match.start()
        body = doc.text[body_start:body_end]
        heading = re.search(rf"^### {evidence_id}$", body, re.MULTILINE)
        content_heading = re.search(r"^#### Learner Content$", body, re.MULTILINE)
        assessment_heading = re.search(r"^#### Tutor Assessment$", body, re.MULTILINE)
        if heading is None or content_heading is None or assessment_heading is None or not (heading.start() < content_heading.start() < assessment_heading.start()):
            errors.append(ValidationError(_line_number(doc.text, body_start), "SCHEMA", f"{evidence_id} structure is invalid"))
            continue
        values_start = body_start + heading.end()
        values_end = body_start + content_heading.start()
        values, lines, spans = _parse_bullets(doc.text, values_start, values_end, EVIDENCE_KEYS, errors, context=evidence_id)
        content_region_start = body_start + content_heading.end()
        content_region_end = body_start + assessment_heading.start()
        marked = _marker_body(
            doc.text[content_region_start:content_region_end],
            "<!-- learner-content:start -->",
            "<!-- learner-content:end -->",
            errors,
        )
        content = ""
        if marked is not None:
            content = marked[0]
        assessment_start = body_start + assessment_heading.end()
        assessment = doc.text[assessment_start:body_end].strip()
        item_line = _line_number(doc.text, start + start_match.start())
        if not content:
            errors.append(ValidationError(item_line, "SCHEMA", f"{evidence_id} Learner Content must not be empty"))
        if not assessment:
            errors.append(ValidationError(item_line, "SCHEMA", f"{evidence_id} Tutor Assessment must not be empty"))
        if values.get("concept") not in doc.contract_concepts:
            errors.append(ValidationError(lines.get("concept", item_line), "EVIDENCE_STATE", f"{evidence_id} concept is not in the reviewed contract"))
        if values.get("kind") not in EVIDENCE_KINDS:
            errors.append(ValidationError(lines.get("kind", item_line), "SCHEMA", f"{evidence_id} kind is not allowed"))
        if values.get("provenance") != "learner":
            errors.append(ValidationError(lines.get("provenance", item_line), "EVIDENCE_STATE", f"{evidence_id} provenance must be learner"))
        verdict = values.get("verdict")
        append_state = values.get("append_state")
        if verdict not in EVIDENCE_VERDICTS:
            errors.append(ValidationError(lines.get("verdict", item_line), "SCHEMA", f"{evidence_id} verdict is not allowed"))
        if append_state not in APPEND_STATES:
            errors.append(ValidationError(lines.get("append_state", item_line), "SCHEMA", f"{evidence_id} append_state is not allowed"))
        if verdict == "confirmed" and append_state not in {"pending", "drafted"}:
            errors.append(ValidationError(lines.get("append_state", item_line), "EVIDENCE_STATE", f"confirmed {evidence_id} must be pending or drafted"))
        if verdict in {"partial", "misconception", "unconfirmed"} and append_state != "not_eligible":
            errors.append(ValidationError(lines.get("append_state", item_line), "EVIDENCE_STATE", f"non-confirmed {evidence_id} must be not_eligible"))
        if "captured_at" in values and not _is_rfc3339(values["captured_at"]):
            errors.append(ValidationError(lines["captured_at"], "SCHEMA", f"{evidence_id} captured_at must be an RFC 3339 timestamp"))
        actual_content_hash = _sha256_bytes(content.encode("utf-8"))
        if "content_sha256" in values and not HASH_RE.fullmatch(values["content_sha256"]):
            errors.append(ValidationError(lines["content_sha256"], "SCHEMA", f"{evidence_id} content_sha256 must be lowercase SHA-256"))
        elif values.get("content_sha256") != actual_content_hash:
            errors.append(ValidationError(lines.get("content_sha256", item_line), "EVIDENCE_STATE", f"{evidence_id} content hash mismatch: got {actual_content_hash}"))
        evidence_items.append(
            Evidence(
                evidence_id=evidence_id,
                values=values,
                content=content,
                assessment=assessment,
                line=item_line,
                append_value_span=spans.get("append_state", (0, 0)),
            )
        )

    evidence_items.sort(key=lambda item: item.evidence_id)
    expected = [f"E{index:03d}" for index in range(1, len(evidence_items) + 1)]
    actual = [item.evidence_id for item in evidence_items]
    if actual != expected:
        errors.append(ValidationError(_line_number(doc.text, start), "SCHEMA", "learner evidence IDs must be unique and contiguous from E001"))
    doc.evidence = {item.evidence_id: item for item in evidence_items}


def _validate_declared_hashes(doc: HandoffDocument, metadata_lines: dict[str, int], errors: list[ValidationError]) -> None:
    declared_manifest = doc.metadata.get("input_manifest_sha256")
    if HASH_RE.fullmatch(declared_manifest or "") and declared_manifest != doc.computed_manifest_sha256:
        errors.append(ValidationError(metadata_lines.get("input_manifest_sha256", 1), "SOURCE_HASH", f"input manifest hash mismatch: got {doc.computed_manifest_sha256}"))
    declared_contract = doc.metadata.get("contract_sha256")
    if HASH_RE.fullmatch(declared_contract or "") and declared_contract != doc.computed_contract_sha256:
        errors.append(ValidationError(metadata_lines.get("contract_sha256", 1), "CONTRACT_HASH", f"contract hash mismatch: got {doc.computed_contract_sha256}"))


def _draft_marker_blocks(text: str, lesson_id: str) -> tuple[list[tuple[str, str, str, int]], bool]:
    escaped = re.escape(lesson_id)
    opening = list(re.finditer(rf"^<!-- lesson-evidence:{escaped}:(E\d{{3}}):([0-9a-f]{{64}}) -->[ \t]*$", text, re.MULTILINE))
    closing = list(re.finditer(rf"^<!-- /lesson-evidence:{escaped}:(E\d{{3}}) -->[ \t]*$", text, re.MULTILINE))
    blocks: list[tuple[str, str, str, int]] = []
    balanced = len(opening) == len(closing)
    for start_match in opening:
        evidence_id, content_hash = start_match.group(1), start_match.group(2)
        end_match = next((candidate for candidate in closing if candidate.group(1) == evidence_id and candidate.start() > start_match.end()), None)
        if end_match is None:
            balanced = False
            continue
        body_start = start_match.end()
        if text[body_start : body_start + 1] == "\n":
            body_start += 1
        body_end = end_match.start()
        if body_end > body_start and text[body_end - 1 : body_end] == "\n":
            body_end -= 1
        blocks.append((evidence_id, content_hash, text[body_start:body_end], _line_number(text, start_match.start())))
    return blocks, balanced


def _validate_draft(doc: HandoffDocument, errors: list[ValidationError]) -> None:
    draft_raw = doc.metadata.get("draft_path")
    if not draft_raw:
        return
    draft_path, path_error = _safe_repo_path(draft_raw, doc.repo_root)
    if path_error:
        errors.append(ValidationError(1, "PATH", f"invalid draft_path: {path_error}"))
        return
    assert draft_path is not None
    drafted = [item for item in doc.evidence.values() if item.values.get("append_state") == "drafted"]
    if not draft_path.exists():
        if drafted:
            errors.append(ValidationError(drafted[0].line, "DRAFT_MARKER", "draft is missing but evidence is marked drafted"))
        return
    if not draft_path.is_file():
        errors.append(ValidationError(1, "PATH", "draft_path is not a regular file"))
        return
    try:
        draft_text = _normalize_newlines(draft_path.read_text(encoding="utf-8"))
    except UnicodeDecodeError:
        errors.append(ValidationError(1, "DRAFT_CONTENT", "draft is not valid UTF-8"))
        return
    lesson_id = doc.metadata.get("lesson_id", "")
    blocks, balanced = _draft_marker_blocks(draft_text, lesson_id)
    if not balanced:
        errors.append(ValidationError(1, "DRAFT_MARKER", "draft lesson-evidence markers are unbalanced"))
    by_id: dict[str, list[tuple[str, str, str, int]]] = {}
    for block in blocks:
        by_id.setdefault(block[0], []).append(block)
    for evidence_id, instances in by_id.items():
        if len(instances) != 1:
            errors.append(ValidationError(instances[0][3], "DRAFT_MARKER", f"duplicate draft marker for {evidence_id}"))
        item = doc.evidence.get(evidence_id)
        if item is None:
            errors.append(ValidationError(instances[0][3], "DRAFT_MARKER", f"draft marker has no handoff evidence: {evidence_id}"))
            continue
        _, marker_hash, body, line = instances[0]
        expected_hash = item.values.get("content_sha256")
        if marker_hash != expected_hash:
            errors.append(ValidationError(line, "DRAFT_CONTENT", f"draft marker hash differs from {evidence_id}"))
        if body != item.content or _sha256_bytes(body.encode("utf-8")) != expected_hash:
            errors.append(ValidationError(line, "DRAFT_CONTENT", f"draft body differs from {evidence_id} Learner Content"))
        if item.values.get("append_state") == "not_eligible":
            errors.append(ValidationError(line, "DRAFT_MARKER", f"not-eligible evidence was appended: {evidence_id}"))
    for item in drafted:
        if item.evidence_id not in by_id:
            errors.append(ValidationError(item.line, "DRAFT_MARKER", f"drafted evidence has no draft marker: {item.evidence_id}"))


def validate_handoff(
    path: Path | str,
    *,
    repo_root: Path | str | None = None,
    ready: bool = False,
    check_draft: bool = True,
) -> ValidationReport:
    handoff_path = Path(path)
    root = Path(repo_root).resolve() if repo_root is not None else _repo_root_from_script()
    errors: list[ValidationError] = []
    if not handoff_path.is_absolute():
        handoff_path = root / handoff_path
    try:
        resolved = handoff_path.resolve(strict=False)
        resolved.relative_to(root)
    except (OSError, ValueError):
        return ValidationReport(handoff_path, ready, [ValidationError(1, "PATH", "handoff path escapes the repository")], None)
    if not handoff_path.exists() or not handoff_path.is_file():
        return ValidationReport(handoff_path, ready, [ValidationError(1, "SOURCE_MISSING", "handoff file does not exist")], None)
    try:
        text = _normalize_newlines(handoff_path.read_text(encoding="utf-8"))
    except UnicodeDecodeError:
        return ValidationReport(handoff_path, ready, [ValidationError(1, "SCHEMA", "handoff is not valid UTF-8")], None)

    doc = HandoffDocument(path=handoff_path, repo_root=root, text=text)
    if not text.startswith("# Active Lesson Handoff\n"):
        errors.append(ValidationError(1, "SCHEMA", "handoff must start with '# Active Lesson Handoff'"))
    if "Codex-generated temporary operational cache" not in text[:500]:
        errors.append(ValidationError(1, "SCHEMA", "handoff must include the temporary operational-cache banner"))
    sections = _section_ranges(text, errors)
    metadata_lines = _parse_metadata(doc, sections.get("Metadata"), errors)
    _parse_manifest(doc, sections.get("Input Manifest"), errors)
    _parse_contract(doc, errors)
    _validate_declared_hashes(doc, metadata_lines, errors)
    _parse_review_attempts(doc, sections.get("Semantic Review"), errors)
    _parse_current_position(doc, sections.get("Current Position"), errors)
    _parse_evidence(doc, sections.get("Learner Evidence"), errors)
    if check_draft:
        _validate_draft(doc, errors)

    if ready:
        status = doc.metadata.get("status")
        if status not in {"active", "paused"}:
            errors.append(ValidationError(metadata_lines.get("status", 1), "REVIEW_NOT_PASS", "--ready requires active or paused status"))
        latest = doc.reviews[-1] if doc.reviews else None
        if latest is None or latest.values.get("verdict") != "pass":
            errors.append(ValidationError(latest.line if latest else 1, "REVIEW_NOT_PASS", "--ready requires a latest pass verdict"))
        elif (
            latest.values.get("reviewed_input_manifest_sha256") != doc.computed_manifest_sha256
            or latest.values.get("reviewed_contract_sha256") != doc.computed_contract_sha256
        ):
            errors.append(ValidationError(latest.line, "REVIEW_STALE", "--ready review hashes are stale"))

    deduplicated: list[ValidationError] = []
    seen: set[tuple[int, str, str]] = set()
    for error in errors:
        key = (error.line, error.code, error.message)
        if key not in seen:
            seen.add(key)
            deduplicated.append(error)
    return ValidationReport(handoff_path, ready, deduplicated, doc)


class _ContractArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        self.exit(2, f"ERROR <cli>:1 [SCHEMA] {message}\n")


def _build_parser() -> argparse.ArgumentParser:
    parser = _ContractArgumentParser(description=__doc__)
    parser.add_argument("handoff", type=Path, help="repository-relative active handoff Markdown path")
    parser.add_argument("--ready", action="store_true", help="also require a current pass and teachable status")
    parser.add_argument("--json", action="store_true", dest="as_json", help="emit machine-readable JSON")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    try:
        report = validate_handoff(args.handoff, ready=args.ready)
    except Exception as exc:  # pragma: no cover - last-resort CLI boundary
        if args.as_json:
            print(json.dumps({"ok": False, "path": args.handoff.as_posix(), "ready": False, "computed": {}, "errors": [{"line": 1, "code": "SCHEMA", "message": f"internal error: {exc}"}]}, ensure_ascii=False, indent=2))
        else:
            print(f"ERROR {args.handoff.as_posix()}:1 [SCHEMA] internal error: {exc}", file=sys.stderr)
        return 2
    if args.as_json:
        print(json.dumps(report.as_json(), ensure_ascii=False, indent=2, sort_keys=True))
    elif report.ok:
        mode = "ready" if args.ready else "valid"
        print(f"OK {report.path.as_posix()} [{mode}]")
    else:
        for error in report.errors:
            print(error.rendered(report.path), file=sys.stderr)
    return report.exit_code


if __name__ == "__main__":
    raise SystemExit(main())
