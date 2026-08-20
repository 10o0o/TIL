# Active lesson handoff contract

Use this contract only for a named, multi-turn lesson that combines material
evaluation with adaptive teaching. The single live file is
`tmp/active-lesson-handoff.md`. It is an ignored operational cache, not a
durable note and not proof of learner understanding.

Copy `../assets/active-lesson-handoff-template.md`, replace every placeholder,
and validate it before teaching:

```bash
python3 .agents/skills/coach-llm-research-study/scripts/validate_lesson_handoff.py \
  tmp/active-lesson-handoff.md
python3 .agents/skills/coach-llm-research-study/scripts/validate_lesson_handoff.py \
  --ready tmp/active-lesson-handoff.md
```

`--json` emits the same result as JSON, including computed hashes. The
validator never edits the handoff.

## Lifecycle

1. Build the manifest and lesson contract with status `preparing`.
2. Record the computed manifest and contract hashes, change the status to
   `review_pending`, and run structural validation.
3. Give a fresh read-only reviewer the handoff and every manifest input. The
   reviewer must not be the contract author and must not be given an intended
   answer.
4. Add one semantic-review attempt. A `changes_required` verdict permits one
   contract correction and one new fresh review. There are at most two review
   attempts. Reviewer unavailability or a second non-pass verdict requires
   status `blocked`; do not teach.
5. A current `pass` permits status `active`. Run `--ready` before the first
   teaching chunk and again after resuming a paused lesson.
6. Update Current Position and learner evidence without rewriting the reviewed
   contract. These changes do not invalidate a current review.
7. Set status `completed` only after the lesson is finished. The save workflow
   may remove a completed handoff only after every confirmed evidence item is
   drafted and the dated TIL commit succeeds.

Resume an existing handoff only when the named primary input path and hash are
unchanged. A source, curriculum, manifest, or lesson-contract change makes a
prior review stale. Never overwrite an `active`, `paused`, or `blocked` handoff
with a different lesson without an explicit close-or-replace decision.
A `completed` handoff may be replaced for a new lesson only when every
confirmed evidence item is already `drafted`. Otherwise preserve it until the
append helper recovers the pending evidence; completion alone is not permission
to discard learner content.

## Metadata

Metadata is a Markdown bullet list with exactly these keys:

- `schema_version`: currently `1`.
- `lesson_id`: stable lowercase identifier matching
  `[a-z0-9][a-z0-9-]{2,63}`.
- `title`: one non-empty line.
- `status`: `preparing`, `review_pending`, `active`, `paused`, `blocked`, or
  `completed`.
- `study_date`: `YYYY-MM-DD`.
- `created_at`, `updated_at`: RFC 3339 timestamps with `Z` or an explicit UTC
  offset.
- `author_id`: stable identity for the contract-writing agent.
- `draft_path`: exactly `til/today.md`.
- `input_manifest_sha256`, `contract_sha256`: lowercase SHA-256 values.

## Input manifest and hashes

The Input Manifest table has these exact columns:

```text
ID | Role | Path | SHA-256
```

- IDs are contiguous `I001`, `I002`, and so on.
- Roles are `primary`, `asset`, `course-index`, `curriculum`, `knowledge`,
  `til`, or `practice`.
- Include at least one `primary` input and exactly one `curriculum` input. The
  curriculum row path is exactly `CURRICULUM.md`.
- Include every local figure or asset referenced by the source. A PDF is one
  input hashed as file bytes.
- Never include `draft_path` (`til/today.md`) in the manifest. The draft,
  Current Position, and Learner Evidence are mutable operational state outside
  the reviewed input and contract hashes. The `til` role is only for a prior,
  finalized dated TIL used as baseline evidence.
- Paths are POSIX, repository-relative paths. Absolute paths, backslashes,
  `.` or `..` components, duplicate paths, non-files, and symlinks that resolve
  outside the repository are invalid.
- Each row hash is SHA-256 over the exact file bytes.

The manifest aggregate is SHA-256 over UTF-8 bytes of the following canonical
text. Sort rows by `(role, path, sha256)`, omit IDs, and retain the final LF:

```text
<role>\t<path>\t<sha256>\n
```

The contract hash is SHA-256 over the exact text inside the
`lesson-contract:start` and `lesson-contract:end` marker lines after converting
CRLF or CR newlines to LF. The LF immediately following the start marker and
the LF immediately preceding the end marker delimit the markers and are not
part of the hashed body. All other whitespace is significant.

## Lesson Contract

Keep the contract between its marker lines and retain these headings in order:

1. `Objective`
2. `Curriculum Targets`
3. `Learner Evidence Baseline`
4. `Corrections, Prerequisites, and Supplements`
5. `Concept Path`
6. `Prepared Teaching Notes`
7. `Deferred`

List one to three stable `CC-*` or `TR-*` curriculum IDs that actually occur in
the manifested `CURRICULUM.md` under Curriculum Targets. Concept Path contains
three to seven contiguous concepts using:

```text
1. C01 | [선수개념] | 개념 이름 | source: path#exact-location
```

The marker is `none`, `[선수개념]`, `[정정]`, or `[보충]`. Every source
location must identify a page, section, formula, code fragment, or other exact
location, and the path before `#` must be present in the Input Manifest.
Prepared Teaching Notes must have one `#### Cnn` subsection for each concept
with non-empty `tiny_example` and `check_question` fields. Keep full-length
teaching prose out of the contract.

## Semantic Review

`review_attempt` equals the number of attempt blocks and is restricted to
`0`, `1`, or `2`. Attempt IDs are contiguous. Each block contains:

- `reviewer_id`: stable identity different from `author_id` and from every
  other reviewer in this handoff;
- `reviewer_mode`: exactly `fresh-subagent`;
- `reviewed_at`: RFC 3339 timestamp;
- `verdict`: `pending`, `pass`, `changes_required`, or `unavailable`;
- `reviewed_input_manifest_sha256` and `reviewed_contract_sha256`;
- a separate Blocking Findings body.

Use this exact block syntax immediately after the top-level
`- review_attempt: N` field. Replace every placeholder and use the same attempt
number in the marker and heading:

```markdown
<!-- semantic-review-attempt:1:start -->
### Review Attempt 1

- reviewer_id: replace-with-fresh-reviewer-id
- reviewer_mode: fresh-subagent
- reviewed_at: YYYY-MM-DDTHH:MM:SSZ
- verdict: pass
- reviewed_input_manifest_sha256: replace-with-current-manifest-sha256
- reviewed_contract_sha256: replace-with-current-contract-sha256

#### Blocking Findings

- none
<!-- semantic-review-attempt:1:end -->
```

For `changes_required` or `unavailable`, replace `none` with the concrete
blocking finding. A second attempt uses `2` in both marker lines and its
heading, plus a different fresh `reviewer_id`.

Only the latest attempt controls readiness. The first attempt may be followed
by another only when its verdict was `changes_required`. A pass is current only
when both reviewed hashes equal the handoff's recomputed hashes. An unavailable
reviewer ends the review flow immediately.

The reviewer checks source fidelity, facts, formulas, tensor shapes, code
claims, marker classification, curriculum alignment, lesson scope, and learner
evidence provenance. Tutor explanations and source summaries are never learner
evidence.

## Current Position

Keep exactly these fields and update them after each meaningful checkpoint:

- `last_completed`
- `next_concept`
- `next_question`

They may change without semantic re-review. `next_question` must be concrete
enough to continue after context loss. `last_completed` is `none` or a Concept
Path concept ID; `next_concept` is a Concept Path concept ID, except that a
completed lesson uses `none`.

## Learner Evidence

Each evidence block has a contiguous ID such as `E001` and these fields:

- `concept`: a contract concept ID such as `C01`;
- `kind`: `explain_back`, `calculation`, `shape_prediction`,
  `code_interpretation`, `transfer`, or `limit`;
- `provenance`: exactly `learner`;
- `verdict`: `confirmed`, `partial`, `misconception`, or `unconfirmed`;
- `append_state`: `pending`, `drafted`, or `not_eligible`;
- `captured_at`: RFC 3339 timestamp;
- `content_sha256`: SHA-256 of the LF-normalized Learner Content marker body,
  using the same boundary-newline rule as the contract.

Preserve the complete learner answer between the Learner Content markers.
Place evaluation separately under Tutor Assessment. A core error makes the
answer `partial` or `misconception`; never silently repair it. A corrected
explain-back is a new evidence item.

Use this exact block syntax under `## Learner Evidence`, with contiguous IDs.
Replace the content hash with the LF-normalized Learner Content body hash:

```markdown
<!-- learner-evidence:E001:start -->
### E001

- concept: C01
- kind: explain_back
- provenance: learner
- verdict: confirmed
- append_state: pending
- captured_at: YYYY-MM-DDTHH:MM:SSZ
- content_sha256: replace-with-learner-content-sha256

#### Learner Content

<!-- learner-content:start -->
Preserve the learner's exact answer here.
<!-- learner-content:end -->

#### Tutor Assessment

State why this answer is confirmed, partial, a misconception, or unconfirmed.
<!-- learner-evidence:E001:end -->
```

Only `provenance: learner` plus `verdict: confirmed` may use `pending` or
`drafted`. Every other verdict uses `not_eligible`. Append eligible evidence
with:

```bash
python3 .agents/skills/teach-course-material/scripts/append_lesson_evidence.py \
  tmp/active-lesson-handoff.md --evidence E001
```

The helper writes this idempotency envelope to `til/today.md`:

```html
<!-- lesson-evidence:<lesson_id>:E001:<content_sha256> -->
<exact learner content>
<!-- /lesson-evidence:<lesson_id>:E001 -->
```

It writes the draft atomically before marking the evidence `drafted`. If a
process stops between those writes, rerunning the helper finds and verifies the
existing envelope, then repairs the handoff state without duplicating content.
The save workflow removes only the envelope comments and preserves their body
verbatim.

## Validator results

Exit status `0` means success. Status `1` reports path, source, hash, review,
evidence, or draft-state errors. Status `2` reports CLI, schema, or unexpected
internal errors. Human-readable errors use:

```text
ERROR path:line [CODE] message
```

Codes are `SCHEMA`, `PATH`, `SOURCE_MISSING`, `SOURCE_HASH`, `CONTRACT_HASH`,
`REVIEW_STALE`, `REVIEW_NOT_PASS`, `EVIDENCE_STATE`, `DRAFT_MARKER`, and
`DRAFT_CONTENT`.
