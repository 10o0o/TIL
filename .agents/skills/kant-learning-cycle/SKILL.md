---
name: kant-learning-cycle
description: Run the repository's active-learning workflow for KANT AI/ML/LLM lecture PDFs and existing notes. Use for curriculum mapping, prerequisite diagnosis, adaptive tutoring, numeric and tensor-shape exercises, teach-back assessment, selective legacy-note migration, minimal TIL generation, lab creation, spaced review, and progress tracking. Do not turn every lecture into a long summary or create canonical notes before learning evidence exists.
---

# KANT Learning Cycle

Operate this repository as an active-learning system, not a lecture transcription pipeline.

## Read the operating context

Before substantial work, read:

1. `GUIDE.md`
2. `curriculum/course-map.md`
3. `curriculum/progress.md`
4. `curriculum/source-index.md`
5. relevant files under `concepts/`, `labs/`, and legacy `content/`
6. applicable templates
7. root `AGENTS.md`

Preserve the user's existing material and unrelated changes.

## Choose one mode

### Curriculum mapping mode

Use when several PDFs or a whole course are supplied.

1. Extract concept inventory.
2. Identify prerequisites and dependency edges.
3. Detect repeated concepts across lectures.
4. Assign P0, P1, or P2 priority for the user's target roles.
5. Compare existing repository notes for duplication, conflict, and misclassification.
6. Update only `curriculum/source-index.md`, `course-map.md`, and `progress.md`.
7. Select one next learning unit.
8. Do not mass-generate canonical notes.

### Learning mode

Use for one concept.

1. Ask 3–5 diagnostic questions before teaching unless the user explicitly asks for an immediate narrow answer.
2. Separate correct understanding, conceptual errors, ambiguous wording, and missing prerequisites.
3. Teach only the gaps, using:
   - problem and motivation
   - intuition
   - a small numeric example
   - exact definition and formula
   - Tensor shapes and axis meaning
   - Python, NumPy, or PyTorch when useful
   - ML, DL, LLM, evaluation, or systems connection
4. Require at least one new application.
5. Ask for a closed-book teach-back.
6. Correct the teach-back precisely.
7. Persist only the minimum justified artifacts.

### Review mode

Use for delayed recall or weekly review.

1. Test recall before showing notes.
2. Include definition, numeric or shape application, and concept connection.
3. Record success and failure honestly.
4. Upgrade or downgrade `curriculum/progress.md` based on evidence.
5. Add a short file under `reviews/` when useful.

### Migration mode

Use when legacy `content/` notes need consolidation.

1. Search all files relevant to one concept.
2. Treat them as candidate sources, not current truth.
3. Identify overlap, conflict, unsupported claims, and useful examples.
4. Re-test the learner before adopting the material.
5. Consolidate into one `concepts/` document only after explanation and application evidence.
6. Preserve original files unless relocation is explicitly requested and links are repaired.

## Evidence gates

Use the following status meanings.

- `seen`: encountered in a lecture or note
- `recognized`: understandable with prompts
- `explained`: accurately explained without notes
- `applied`: solved a new example or interpretation problem
- `implemented`: implemented or debugged a minimal version
- `retained`: reproduced after a delayed review

Never infer mastery from note length, file existence, or a successful copy-edit.

A canonical concept note normally requires `explained` and `applied`. Code-heavy topics may also require `implemented`.

## Decide what to write

| Evidence | Repository action |
|---|---|
| Exposure only | update `curriculum/progress.md` as `seen` |
| Understanding only with explanation | keep `recognized`; do not create a polished note |
| One misconception corrected | write a 5–15 line TIL if useful |
| Explained and applied | create or update one canonical concept note |
| Executed code | add a reproducible lab |
| Delayed recall | update review and progress |

Do not create empty directories, placeholder-heavy documents, or output merely to satisfy a template.

## Canonical-note rules

- One concept per document.
- Prefer stable paths such as `concepts/ml/bias-variance.md`.
- Update an existing concept instead of creating lecture-specific duplicates.
- Connect intuition to actual tensors, operations, learned parameters, and output meaning.
- For matrix operations, state operand shapes, contracted dimensions, result shape, and remaining-axis meaning.
- Map formulas to code line by line.
- Distinguish a pedagogical simplification from actual model behavior.
- Link substantial executable work from `labs/`.

## TIL rules

- Keep it to the day's changed mental model.
- Do not reproduce the whole lecture.
- Include previous misunderstanding, corrected understanding, evidence, and next question.
- Skip the TIL when nothing materially changed.
- Never backfill missed dates merely for completeness.

## Validation

For each change:

1. inspect the complete changed file
2. verify Markdown links and relative paths
3. execute relevant code and compare recorded output
4. run the repository validator where applicable
5. run `git diff --check`
6. report checks that could not be performed

## Final report

After repository changes, report:

- learning unit or migration scope
- evidence obtained
- files created or updated
- progress status changes and their basis
- unresolved prerequisites
- exact next learning action
