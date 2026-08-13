---
name: organize-til-notes
description: Organize, revise, consolidate, and validate a specific Korean learning note in this repository while preserving the author's questions, examples, calculations, and learning evidence. Use when the user explicitly asks to refine an existing note, create a concise evidence-based TIL from supplied learning results, or consolidate one revalidated concept. Do not use for generic repository maintenance, Git-only work, or read-only conceptual explanations.
---

# Organize TIL Notes

Turn an explicitly scoped learning record into a readable, verifiable artifact without replacing the learner's reasoning with a generic lecture summary.

## Establish the task boundary

1. Resolve the exact target with `rg --files`; preserve Korean spelling, spaces, brackets, and parentheses in paths.
2. Read the complete target, root `AGENTS.md`, the relevant template, and one relevant neighboring document before editing substantially.
3. Distinguish the requested action:
   - For explanation, review, feasibility, or direction checks, inspect and respond without editing.
   - For requests to refine, organize, correct, consolidate, or apply changes, edit only the exact authorized target.
4. Search for an existing canonical concept before creating another.
5. Preserve unrelated working-tree files and changes. Never broaden the edit or commit scope silently.

## Choose the artifact deliberately

### Existing-note refinement

Use when the user names an existing document and requests correction, restructuring, or validation.

- Preserve original questions, examples, intermediate calculations, confusion points, date, and intent.
- Correct factual, mathematical, terminology, spelling, spacing, shape, code-output, link, and rendering errors in the authorized scope.
- Remove template instructions that are not real content.
- Do not turn the note into a generic textbook chapter.
- Do not relocate a legacy file merely because its current directory is imperfect.

### Concise daily TIL

Use `templates/til.md` only when the supplied learning record shows an actual change in understanding.

- Capture closed-book recall, the prior misconception or gap, corrected understanding, evidence, remaining question, and next review date.
- Keep the result short; link to a concept or lab instead of copying it.
- Skip the TIL when the only event was reading, attending a lecture, or recognizing an explanation.

### Canonical concept consolidation

Use `templates/concept.md` only for one concept that the learner has already explained without notes and applied to a new problem.

- Search all relevant legacy notes and identify overlap, conflict, and useful examples.
- Revalidate formulas, shapes, and code before adopting them.
- Consolidate into one file under `concepts/`.
- Put substantial executed code under `labs/`.
- Preserve original `content/` files unless movement is explicitly requested and links are repaired.

### Executable lab or review

- Use `templates/lab.md` only after code has actually been run and the output can be recorded honestly.
- Use `templates/weekly-review.md` for delayed recall, including failed recall and any justified status downgrade.
- Do not fabricate an experiment or a successful review to fill a section.

## Preserve the learning record

- Retain the author's concrete language when it captures a useful mental model.
- Start difficult additions with a small trace or numeric example, show intermediate states or shapes, and then generalize.
- Do not hide learner-relevant steps behind a finished formula, advanced abstraction, or replacement solution.
- Do not invent a confusion point, reference, experiment, practical application, or mastery claim.
- Omit or remove sections that have no meaningful evidence rather than forcing every template heading.

## Frontmatter and structure

- Preserve the original `date` when known.
- Update `updated` only for a material content change.
- Do not change `publish` unless the user requests it.
- Use one top-level heading that represents the frontmatter title.
- Write primarily in clear Korean. Add an English technical term on first use when helpful.
- Keep symbols, terminology, capitalization, and code names consistent.
- Follow the role and creation gate of the selected template; do not mix a daily delta, canonical explanation, and full experiment into one file.

## Explain mathematics and code

- Follow root `AGENTS.md` for GitHub-compatible Markdown, mathematics, emphasis, links, and media.
- For matrix multiplication, state both operand shapes, the contracted dimension, the result shape, and the meaning of each remaining axis.
- Distinguish `@` from `*`, inner product from cosine similarity, and raw scores from normalized or scaled scores.
- Put executable examples in fenced blocks with a language identifier.
- Run code with `python3` or an appropriate verified environment; never infer recorded output when it can be executed safely.
- Compare displayed numeric values, array contents, and shapes with actual output.
- State clearly when a visual renderer or external page was not inspected.

## Validate the result

Run the bundled validator on every changed TIL or compatible concept document from the repository root:

```bash
python3 .agents/skills/organize-til-notes/scripts/validate_til_markdown.py path/to/changed.md
```

The validator checks frontmatter, final newlines, heading count, fenced code blocks, math delimiters, prohibited macros, Korean bold-emphasis boundaries, placeholder remnants, and relative links.

Then:

1. Read the complete revised document from top to bottom.
2. Execute relevant code and compare its output with the note.
3. Check changed relative links and local assets.
4. Review `git diff --check`, `git diff --name-only`, and `git diff --stat`.
5. If committing was explicitly requested, follow exact-path staging and commit rules in root `AGENTS.md`.

Report which checks passed and any check that could not be run. Do not claim GitHub rendering success until the pushed page has actually been inspected on GitHub.
