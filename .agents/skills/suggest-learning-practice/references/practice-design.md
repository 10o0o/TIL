# Practice design contract

Use this reference to design and independently review generated practice. The
research motivates the sequence; it does not justify inflating every lesson
into a large project.

## Learning-design basis

- **Authentic whole task**: 4C/ID organizes complex-skill learning around
  meaningful whole tasks, supported information, procedural information, and
  part-task practice. Here that means shrinking one real ML workflow while
  preserving its input contract, core implementation, tests, failure
  diagnosis, and interpretation. It does not mean adding production scale.
  See [4C/ID in the context of instructional design and the learning
  sciences](https://research.ou.nl/en/publications/4cid-in-the-context-of-instructional-design-and-the-learning-scie/).
- **Deliberate practice**: practice needs a concrete performance target,
  effortful learner execution, observable error, and feedback focused on
  improvement. Repetition alone and a generic project do not meet this bar.
  See [Ericsson, Krampe, and Tesch-Römer
  (1993)](https://doi.org/10.1037/0033-295X.100.3.363). Do not turn this into a
  “10,000 hours” claim or claim practice explains all expertise.
- **Retrieval practice**: ask for a prediction or reconstruction before showing
  setup-specific cues. Retrieval can strengthen later retention more than
  restudy alone, so an already well-written TIL still benefits from a blank
  implementation attempt. See [Roediger and Karpicke
  (2006)](https://doi.org/10.1111/j.1467-9280.2006.01693.x).
- **Fading**: progress from a tiny analogous trace to pseudocode and only then
  a minimal API skeleton. Never jump directly from no help to a full answer.
  See [Renkl et al. (2002)](https://eric.ed.gov/?id=EJ658398).
- **Avoid split attention**: put the hint beside the TODO it explains. A global
  hint appendix forces the learner to alternate between separate information
  sources and adds irrelevant search work. See [Chandler and Sweller
  (1992)](https://doi.org/10.1111/j.2044-8279.1992.tb01017.x).

## Whole-task sizing

Keep the smallest workflow that still exposes the professional boundary:

1. deterministic input or fixture;
2. explicit public contract;
3. learner-owned core logic;
4. normal, edge, and failure observation;
5. diagnosis from the actual failure;
6. explanation of system meaning and limitation.

For a Tensor lesson this might be a boundary function plus tests, not a model
service. For a training-loop lesson it might be `train_step`, validation, and
checkpoint selection on a fixed CPU batch, not distributed training.

For a bundle, put exactly one unexecuted `# setup-check` cell before the first
exercise TODO. It must add that exact bundle's `src/` from a repository-root
kernel and import the public learner interface. The artifact validator executes
this preparation cell without its pytest `PYTHONPATH` injection, so a workbook
cannot appear valid while its first import is unusable.

## Coverage-map review

For every major TIL outcome, ask:

1. Is the cited TIL location exact enough to find the learner's statement?
2. Does the action test performance rather than recognition?
3. Is required evidence observable in code, a test, a trace, or an interpreted
   result?
4. Is the outcome naturally part of this whole task? If not, split only when a
   separate environment or interpretation is necessary.
5. Does prior evidence include independent execution and interpretation? A
   correct written explanation alone does not remove the outcome.

## Artifact review rubric

A fresh reviewer returns `pass` only when all are true:

- the exact finalized TIL is valid and all major outcomes are represented;
- exact lesson links resolve and instructor practice comes from an explicit
  `INDEX.md` mapping;
- each public learner function is a genuine blank core implementation;
- tests cover normal, edge, and failure behavior without revealing the method;
- each exercise begins with context and prediction, provides a tiny contract,
  and ends with failure diagnosis and interpretation;
- Hint 1 and Hint 2 are folded and adjacent to that exercise's TODO;
- code cells are unexecuted and contain no fabricated output;
- setup, package structure, and production conventions remain smaller than the
  concept being learned;
- initial pytest collection and imports succeed, while execution fails only at
  explicit learner-owned `NotImplementedError` boundaries.

The reviewer identifies concrete blocking findings, not stylistic preferences.
One revision and one second fresh review are the maximum. Never replace an
unavailable independent reviewer with the author's self-approval.
