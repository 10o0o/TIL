from __future__ import annotations

import hashlib
from pathlib import Path


def sha256(data: bytes | str) -> str:
    if isinstance(data, str):
        data = data.encode("utf-8")
    return hashlib.sha256(data).hexdigest()


CONTRACT = """### Objective

Trace a tensor operation and explain its shape contract.

### Curriculum Targets

- CC-DL-01

### Learner Evidence Baseline

- The learner has not yet demonstrated this shape trace.

### Corrections, Prerequisites, and Supplements

- [선수개념] Axis meaning is required at `materials/lesson.md#axes`.

### Concept Path

1. C01 | [선수개념] | Axis meaning | source: materials/lesson.md#axes
2. C02 | none | Shape propagation | source: materials/lesson.md#shape-propagation
3. C03 | [보충] | Attention connection | source: CURRICULUM.md#cc-dl-01

### Prepared Teaching Notes

#### C01

- tiny_example: Trace a 2 by 3 matrix by row and column.
- check_question: Which axis contains the three features?

#### C02

- tiny_example: Broadcast a 2 by 1 tensor with a 1 by 3 tensor.
- check_question: What is the result shape and why?

#### C03

- tiny_example: Map batch, token, and hidden axes for one small tensor.
- check_question: Which attention operation preserves the token axis?

### Deferred

- Kernel-level performance details.
"""


def build_handoff(
    root: Path,
    *,
    status: str = "preparing",
    reviews: list[tuple[str, str]] | None = None,
    evidence: list[dict[str, str]] | None = None,
    lesson_id: str = "tensor-shape-lesson",
    primary_path: str = "materials/lesson.md",
    primary_bytes: bytes = b"# Lesson\n\n## axes\n\nTensor axes.\n",
    coverage: list[dict[str, str]] | None = None,
    pre_save_verdict: str = "pending",
    reviewed_at: str = "pending",
    reviewed_draft_sha256: str = "pending",
) -> tuple[Path, dict[str, str]]:
    reviews = reviews or []
    evidence = evidence or []
    (root / "materials").mkdir(parents=True, exist_ok=True)
    primary = root / primary_path
    if not primary.exists():
        primary.parent.mkdir(parents=True, exist_ok=True)
        primary.write_bytes(primary_bytes)
    curriculum = root / "CURRICULUM.md"
    if not curriculum.exists():
        curriculum.write_text("# Curriculum\n\n## CC-DL-01\n", encoding="utf-8")
    source_hash = sha256(primary.read_bytes())
    curriculum_hash = sha256(curriculum.read_bytes())
    manifest_rows = [
        ("I001", "primary", primary_path, source_hash),
        ("I002", "curriculum", "CURRICULUM.md", curriculum_hash),
    ]
    manifest_hash = sha256(
        "".join(sorted(f"{role}\t{path}\t{digest}\n" for _, role, path, digest in manifest_rows))
    )
    contract_hash = sha256(CONTRACT)

    review_text = ""
    for attempt, (verdict, reviewer_id) in enumerate(reviews, start=1):
        review_text += f"""
<!-- semantic-review-attempt:{attempt}:start -->
### Review Attempt {attempt}

- reviewer_id: {reviewer_id}
- reviewer_mode: fresh-subagent
- reviewed_at: 2026-08-20T01:00:0{attempt}Z
- verdict: {verdict}
- reviewed_input_manifest_sha256: {manifest_hash}
- reviewed_contract_sha256: {contract_hash}

#### Blocking Findings

- {"none" if verdict == "pass" else "Revise the named contract point."}
<!-- semantic-review-attempt:{attempt}:end -->
"""

    evidence_text = ""
    content_hashes: dict[str, str] = {}
    for index, item in enumerate(evidence, start=1):
        evidence_id = f"E{index:03d}"
        content = item.get("content", "배치 축과 특성 축을 구분해 결과 shape를 설명했다.")
        content_hash = sha256(content)
        content_hashes[evidence_id] = content_hash
        evidence_text += f"""
<!-- learner-evidence:{evidence_id}:start -->
### {evidence_id}

- concept: {item.get("concept", "C01")}
- kind: {item.get("kind", "explain_back")}
- provenance: {item.get("provenance", "learner")}
- verdict: {item.get("verdict", "confirmed")}
- append_state: {item.get("append_state", "pending")}
- captured_at: 2026-08-20T01:30:0{index}Z
- content_sha256: {content_hash}

#### Learner Content

<!-- learner-content:start -->
{content}
<!-- learner-content:end -->

#### Tutor Assessment

{item.get("assessment", "축의 의미와 결과 shape를 독립적으로 설명했다.")}
<!-- learner-evidence:{evidence_id}:end -->
"""

    if coverage is None:
        coverage = [
            {
                "concept": concept,
                "state": "deferred",
                "evidence_ids": "none",
                "representation": "not-required",
                "note": "Not taught yet.",
            }
            for concept in ("C01", "C02", "C03")
        ]
    coverage_rows = "\n".join(
        "| {concept} | {state} | {evidence_ids} | {representation} | {note} |".format(**row)
        for row in coverage
    )

    next_concept = "none" if status == "completed" else "C01"
    rows = "\n".join(f"| {item_id} | {role} | {path} | {digest} |" for item_id, role, path, digest in manifest_rows)
    text = f"""# Active Lesson Handoff

> Codex-generated temporary operational cache. This file is not a durable
> learner note and is not evidence of learner understanding.

## Metadata

- schema_version: 2
- lesson_id: {lesson_id}
- title: Tensor shape lesson
- status: {status}
- study_date: 2026-08-20
- created_at: 2026-08-20T00:00:00Z
- updated_at: 2026-08-20T01:30:00Z
- author_id: contract-author
- draft_path: til/today.md
- input_manifest_sha256: {manifest_hash}
- contract_sha256: {contract_hash}

## Input Manifest

| ID | Role | Path | SHA-256 |
| --- | --- | --- | --- |
{rows}

<!-- lesson-contract:start -->
{CONTRACT}
<!-- lesson-contract:end -->

## Semantic Review

- review_attempt: {len(reviews)}
{review_text}
## Current Position

- last_completed: none
- next_concept: {next_concept}
- next_question: Explain the next shape transition.

## Daily Learning Coverage

- pre_save_verdict: {pre_save_verdict}
- reviewed_at: {reviewed_at}
- reviewed_draft_sha256: {reviewed_draft_sha256}

| Concept ID | Today state | Evidence IDs | TIL representation | Note |
| --- | --- | --- | --- | --- |
{coverage_rows}

## Learner Evidence
{evidence_text}
"""
    handoff = root / "tmp" / "active-lesson-handoff.md"
    handoff.parent.mkdir(parents=True, exist_ok=True)
    handoff.write_text(text, encoding="utf-8")
    return handoff, {
        "manifest_hash": manifest_hash,
        "contract_hash": contract_hash,
        **{f"{item_id}_hash": digest for item_id, digest in content_hashes.items()},
    }


def draft_envelope(lesson_id: str, evidence_id: str, content: str) -> str:
    return (
        f"<!-- lesson-evidence:{lesson_id}:{evidence_id}:{sha256(content)} -->\n"
        f"{content}\n"
        f"<!-- /lesson-evidence:{lesson_id}:{evidence_id} -->\n"
    )
