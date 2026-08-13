---
name: organize-til-notes
description: Refine, validate, or selectively migrate one existing Korean TIL or lecture-note file in this repository. Use only when the user explicitly asks to revise a specific existing document or migrate its verified material into a canonical concept note. For new lecture learning, curriculum mapping, diagnosis, exercises, teach-back, or progress tracking, use kant-learning-cycle instead.
---

# Organize TIL Notes

This is a secondary maintenance skill. The default learning workflow is `$kant-learning-cycle`.

## Establish the exact scope

1. Resolve the exact target path.
2. Read the complete target, root `AGENTS.md`, `GUIDE.md`, and the relevant template.
3. Search for existing canonical concept documents before creating another one.
4. Preserve unrelated files, learning history, examples, and questions.
5. Do not broaden a one-file revision into a repository-wide rewrite.

## Distinguish the task

### Existing-file refinement

Use when the user names one document and requests correction, restructuring, or validation.

- Preserve the author's reasoning and concrete examples.
- Correct factual, mathematical, terminology, spelling, shape, code-output, link, and rendering errors.
- Remove placeholder instructions that are not real content.
- Do not invent confusion points, experiments, references, or mastery evidence.
- Do not convert the document into a generic textbook chapter.

### Canonical migration

Use only after the learner has been assessed through `$kant-learning-cycle`.

- Extract useful material from relevant legacy notes.
- Resolve duplicates and contradictions.
- Consolidate one concept into one file under `concepts/`.
- Put executed code under `labs/`.
- Leave a short TIL only when the learner's understanding changed.
- Preserve original `content/` files unless movement is explicitly requested.

## Structure

Use:

- `templates/concept.md` for canonical concepts
- `templates/til.md` for short daily deltas
- `templates/lab.md` for executed experiments

Do not force every section when no evidence exists.

## Mathematics and code

- Use GitHub-compatible dollar-sign math delimiters.
- For matrix multiplication, state both operand shapes, the contracted dimension, the result shape, and each remaining axis.
- Distinguish `@` from `*`, inner product from cosine similarity, and raw scores from normalized scores.
- Execute code when safe; never fabricate output.
- State when external rendering was not visually inspected.

## Validation

Run the checks required by root `AGENTS.md`, including the bundled validator for applicable Markdown documents.

Report:

- exact files changed
- corrections made
- checks run
- any unresolved claims or missing evidence
