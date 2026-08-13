---
name: organize-til-notes
description: Organize, revise, and validate a specific Korean TIL note while preserving the learner's questions, examples, calculations, and intent. Use when the user explicitly asks to clean up or correct an existing learning note. Do not use for generic repository maintenance or read-only explanations.
---

# Organize TIL Notes

Clean up one explicitly requested note without replacing the learner's thinking with a generic textbook summary.

## Work on the named note

1. Resolve the exact path and read the entire note.
2. Read its source or relevant neighboring note when needed for accuracy.
3. Preserve the learner's questions, examples, calculations, and useful wording.
4. Correct factual, mathematical, shape, code-output, link, and Markdown errors.
5. Remove empty template sections and unnecessary repetition.

Do not move or rewrite unrelated notes. Preserve existing `content/` files unless the user explicitly requests a move.

## Keep it light

Use `templates/til.md` for a new TIL. A note usually needs only:

- what was learned;
- what was corrected or clarified;
- what was tried;
- what to look at next.

Omit sections that add no value. Put substantial executed code under `practice/`; short snippets may stay in the TIL.

## Mathematics and code

- Explain difficult ideas with a small example before generalizing.
- State Tensor shapes and the meaning of their axes when relevant.
- Connect formulas to code directly.
- Run executable examples when safe and record only actual output.
- Never invent an experiment, result, confusion point, or source.

## Validate

Run the bundled validator from the repository root:

```bash
python3 .agents/skills/organize-til-notes/scripts/validate_til_markdown.py path/to/changed.md
```

Then read the final note, check relative links, and run `git diff --check`. Report any check that could not be performed.
