---
name: save-today-til
description: Parse a freely written Markdown study draft, especially this repository's root today.md, into the canonical Korean TIL template and save or merge it at til/YYYY/MM/YYYY-MM-DD.md. Use only when the user explicitly invokes $save-today-til or explicitly asks to finalize, file, or save a named rough note as a daily TIL. Do not use for tutoring feedback, factual auditing, knowledge-base synthesis, practice recommendations, or generic Markdown editing.
---

# Save Today TIL

Turn one rough study memo into this repository's dated TIL without replacing the learner's thinking with a textbook summary.

## Respect the review boundary

This skill formats and files a draft; it does not establish conceptual correctness.

- In the normal daily workflow, use `$coach-llm-research-study` to review the draft against its studied source before invoking this skill.
- Do not perform a source audit merely because no prior review is visible; a standalone save request remains valid, and a TIL may intentionally preserve uncertainty.
- If the current conversation contains a pre-save verdict with unresolved `반드시 수정` or `추가 확인` findings, do not finalize those statements as established facts. Continue only after the learner resolves them, asks to express them explicitly as uncertainty, or knowingly asks to preserve the unverified draft.
- Never treat a `저장 가능` verdict as evidence for `knowledge/`; it only means the draft is suitable as a chronological TIL.

## Resolve the input

1. Work from the repository root.
2. Use the file named by the user. If none is named, use `today.md`.
3. Require a Markdown file inside this repository. Do not read from or write to `archive/` for this workflow.
4. Read the entire draft and `til/template.md` before editing anything.
5. Treat a missing file, an empty file, or the reset comment alone as having nothing to save. Report that and make no other changes.

## Choose the date and destination

Use the first applicable date source:

1. an exact date explicitly supplied by the user;
2. one unambiguous `YYYY-MM-DD` study date written in the draft;
3. the current date in `Asia/Seoul`.

Do not use file modification time as the study date. If multiple dates could change the destination and the intended date is unclear, ask before writing.

Save to:

```text
til/YYYY/MM/YYYY-MM-DD.md
```

Use one file per study date, even when the draft contains several topics. Create missing year and month directories. Never derive a topic-based filename.

## Parse into the template

Follow the headings and order in `til/template.md`.

- Put the session narrative, studied material, calculations, and actions under `오늘의 학습`.
- Put conclusions, changed understanding, and personally meaningful takeaways under `배운 점`.
- Put explicit uncertainty, questions, and unresolved contradictions under `남은 질문`.
- Put only next actions the learner actually wrote under `다음에 할 것`.
- Put only real source, knowledge, or practice links under `관련 기록`.
- Keep `오늘의 학습`. Omit any other section when the draft contains no supporting content.
- When classification is uncertain, keep the content under `오늘의 학습` instead of inventing structure.
- For multiple topics, use `###` subheadings only when they materially improve scanning.
- When the learner explicitly distinguishes the live lecture from later GPT-assisted study, preserve that provenance with `### 라이브 수업` and `### 보충 학습` under `오늘의 학습`. Do not infer the distinction from writing style alone, and do not add empty provenance headings.

Preserve the learner's first-person voice, uncertainty, examples, equations, code, observed results, and reasoning. Fix mechanical spelling, spacing, paragraph breaks, obvious repetition, and Markdown. Do not silently correct concepts, answer questions, add facts, fabricate links or results, or compress the note into a generic concept summary.

Keep pre-save factual evaluation in `$coach-llm-research-study`, reusable concept synthesis in `$update-learning-knowledge`, and optional activities in `$suggest-learning-practice` unless the user separately requests those tasks.

## Write safely

- If the destination does not exist, create it from the template with all placeholders removed.
- If the destination exists, read it fully and merge new material into the matching sections. Preserve existing content and remove only clear duplication. Never overwrite the file wholesale.
- Resolve relative links from the source location and rewrite them relative to the destination. Do not create a link unless its target is known.
- Use `apply_patch` for the note and other text changes.
- Do not delete or reset the source until the destination passes validation.
- After a successful save from the root `today.md`, replace it with only:

```markdown
<!-- 형식 없이 자유롭게 작성하세요. 저장할 때 $save-today-til을 사용합니다. -->
```

- Leave any other named source file unchanged unless the user explicitly asks to remove or reset it.
- Do not update `knowledge/`, create a practice file, commit, or push as part of this skill unless the user explicitly requests that separate action.

## Validate and report

Run from the repository root:

```bash
python3 .agents/skills/save-today-til/scripts/validate_til.py til/YYYY/MM/YYYY-MM-DD.md
git diff --check -- til/YYYY/MM/YYYY-MM-DD.md
```

Read the final file once more. Report the saved path, whether an existing daily note was merged, whether `today.md` was reset, and any check that could not be completed.
