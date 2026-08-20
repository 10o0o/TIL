from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SKILL = Path(__file__).resolve().parents[1]
REPO = SKILL.parents[2]
sys.path.insert(0, str(SKILL / "scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from handoff_fixture import CONTRACT, build_handoff, draft_envelope, sha256  # noqa: E402
from validate_lesson_handoff import validate_handoff  # noqa: E402


class LessonHandoffValidatorTests(unittest.TestCase):
    def make_root(self) -> tempfile.TemporaryDirectory[str]:
        return tempfile.TemporaryDirectory()

    def assert_code(self, report, code: str) -> None:
        self.assertIn(code, {error.code for error in report.errors}, report.errors)

    def build_til_ready_handoff(self, root: Path) -> Path:
        content = "배치 축과 특성 축을 구분해 결과 shape를 설명했다."
        draft = root / "til/today.md"
        draft.parent.mkdir(parents=True, exist_ok=True)
        draft.write_text(
            "# 오늘의 학습\n\n"
            + draft_envelope("tensor-shape-lesson", "E001", content)
            + "\n\n## 남은 질문\n\nBroadcasting에서 오른쪽 축부터 비교하는 이유는 무엇인가?\n",
            encoding="utf-8",
        )
        handoff, _ = build_handoff(
            root,
            status="paused",
            reviews=[("pass", "fresh-reviewer")],
            evidence=[{"concept": "C01", "content": content, "append_state": "drafted"}],
            coverage=[
                {
                    "concept": "C01",
                    "state": "confirmed",
                    "evidence_ids": "E001",
                    "representation": "learning",
                    "note": "Learner explanation is present in the draft.",
                },
                {
                    "concept": "C02",
                    "state": "uncertain",
                    "evidence_ids": "none",
                    "representation": "remaining-question",
                    "note": "draft-anchor: Broadcasting에서 오른쪽 축부터 비교하는 이유는 무엇인가?",
                },
                {
                    "concept": "C03",
                    "state": "deferred",
                    "evidence_ids": "none",
                    "representation": "not-required",
                    "note": "Not taught today.",
                },
            ],
            pre_save_verdict="저장 가능",
            reviewed_at="2026-08-20T02:00:00Z",
            reviewed_draft_sha256=sha256(draft.read_bytes()),
        )
        return handoff

    def test_preparing_handoff_is_structurally_valid_but_not_ready(self) -> None:
        with self.make_root() as directory:
            root = Path(directory)
            handoff, _ = build_handoff(root)
            self.assertTrue(validate_handoff(handoff, repo_root=root).ok)
            ready = validate_handoff(handoff, repo_root=root, ready=True)
            self.assertFalse(ready.ok)
            self.assert_code(ready, "REVIEW_NOT_PASS")

    def test_active_pass_with_current_hashes_is_ready(self) -> None:
        with self.make_root() as directory:
            root = Path(directory)
            handoff, _ = build_handoff(root, status="active", reviews=[("pass", "fresh-reviewer")])
            report = validate_handoff(handoff, repo_root=root, ready=True)
            self.assertTrue(report.ok, report.errors)

    def test_til_ready_accepts_complete_learning_and_uncertainty_inventory(self) -> None:
        with self.make_root() as directory:
            root = Path(directory)
            handoff = self.build_til_ready_handoff(root)
            report = validate_handoff(handoff, repo_root=root, til_ready=True)
            self.assertTrue(report.ok, report.errors)

    def test_til_ready_rejects_missing_confirmed_or_uncertain_concept(self) -> None:
        with self.make_root() as directory:
            root = Path(directory)
            handoff = self.build_til_ready_handoff(root)
            text = handoff.read_text(encoding="utf-8").replace(
                "| C01 | confirmed | E001 | learning |",
                "| C01 | confirmed | E001 | missing |",
            )
            handoff.write_text(text, encoding="utf-8")
            report = validate_handoff(handoff, repo_root=root, til_ready=True)
            self.assert_code(report, "TIL_COVERAGE")

            handoff = self.build_til_ready_handoff(root)
            text = handoff.read_text(encoding="utf-8").replace(
                "| C02 | uncertain | none | remaining-question |",
                "| C02 | uncertain | none | missing |",
            )
            handoff.write_text(text, encoding="utf-8")
            report = validate_handoff(handoff, repo_root=root, til_ready=True)
            self.assert_code(report, "TIL_COVERAGE")

    def test_til_ready_rejects_claimed_uncertainty_without_draft_question(self) -> None:
        with self.make_root() as directory:
            root = Path(directory)
            handoff = self.build_til_ready_handoff(root)
            draft = root / "til/today.md"
            draft.write_text(
                draft.read_text(encoding="utf-8").split("\n\n## 남은 질문", 1)[0] + "\n",
                encoding="utf-8",
            )
            handoff_text = handoff.read_text(encoding="utf-8")
            old_hash = re.search(r"- reviewed_draft_sha256: ([0-9a-f]{64})", handoff_text)
            self.assertIsNotNone(old_hash)
            handoff.write_text(
                handoff_text.replace(old_hash.group(1), sha256(draft.read_bytes()), 1),
                encoding="utf-8",
            )
            report = validate_handoff(handoff, repo_root=root, til_ready=True)
            self.assert_code(report, "TIL_COVERAGE")

    def test_til_ready_rejects_uncertain_anchor_missing_from_question(self) -> None:
        with self.make_root() as directory:
            root = Path(directory)
            handoff = self.build_til_ready_handoff(root)
            text = handoff.read_text(encoding="utf-8").replace(
                "draft-anchor: Broadcasting에서 오른쪽 축부터 비교하는 이유는 무엇인가?",
                "draft-anchor: 초안에 없는 질문",
            )
            handoff.write_text(text, encoding="utf-8")
            report = validate_handoff(handoff, repo_root=root, til_ready=True)
            self.assert_code(report, "TIL_COVERAGE")

    def test_til_ready_ignores_deferred_source_content(self) -> None:
        with self.make_root() as directory:
            root = Path(directory)
            handoff = self.build_til_ready_handoff(root)
            report = validate_handoff(handoff, repo_root=root, til_ready=True)
            self.assertTrue(report.ok, report.errors)
            self.assertEqual(report.document.learning_coverage["C03"].til_representation, "not-required")

    def test_til_ready_rejects_stale_draft_and_missing_contract_review(self) -> None:
        with self.make_root() as directory:
            root = Path(directory)
            handoff = self.build_til_ready_handoff(root)
            with (root / "til/today.md").open("a", encoding="utf-8") as stream:
                stream.write("\nchanged after review\n")
            report = validate_handoff(handoff, repo_root=root, til_ready=True)
            self.assert_code(report, "TIL_REVIEW_STALE")

            handoff, _ = build_handoff(
                root,
                status="paused",
                pre_save_verdict="저장 가능",
                reviewed_at="2026-08-20T02:00:00Z",
                reviewed_draft_sha256=sha256((root / "til/today.md").read_bytes()),
            )
            report = validate_handoff(handoff, repo_root=root, til_ready=True)
            self.assert_code(report, "REVIEW_NOT_PASS")

    def test_til_ready_rejects_confirmed_evidence_not_yet_drafted(self) -> None:
        with self.make_root() as directory:
            root = Path(directory)
            handoff = self.build_til_ready_handoff(root)
            text = handoff.read_text(encoding="utf-8").replace(
                "- append_state: drafted",
                "- append_state: pending",
            )
            handoff.write_text(text, encoding="utf-8")
            report = validate_handoff(handoff, repo_root=root, til_ready=True)
            self.assert_code(report, "TIL_COVERAGE")

    def test_ready_rejects_checkpoint_outside_contract(self) -> None:
        with self.make_root() as directory:
            root = Path(directory)
            handoff, _ = build_handoff(root, status="paused", reviews=[("pass", "fresh-reviewer")])
            text = handoff.read_text(encoding="utf-8").replace("- last_completed: none", "- last_completed: C99")
            handoff.write_text(text, encoding="utf-8")
            report = validate_handoff(handoff, repo_root=root, ready=True)
            self.assertFalse(report.ok)
            self.assert_code(report, "SCHEMA")

    def test_contract_author_cannot_review_own_contract(self) -> None:
        with self.make_root() as directory:
            root = Path(directory)
            handoff, _ = build_handoff(root, status="active", reviews=[("pass", "contract-author")])
            report = validate_handoff(handoff, repo_root=root)
            self.assertFalse(report.ok)
            self.assert_code(report, "REVIEW_NOT_PASS")

    def test_second_attempt_requires_changes_and_a_new_reviewer(self) -> None:
        with self.make_root() as directory:
            root = Path(directory)
            handoff, _ = build_handoff(
                root,
                status="active",
                reviews=[("changes_required", "reviewer-one"), ("pass", "reviewer-two")],
            )
            self.assertTrue(validate_handoff(handoff, repo_root=root, ready=True).ok)
            text = handoff.read_text(encoding="utf-8").replace("reviewer-two", "reviewer-one")
            handoff.write_text(text, encoding="utf-8")
            report = validate_handoff(handoff, repo_root=root)
            self.assert_code(report, "REVIEW_NOT_PASS")

    def test_unavailable_or_second_nonpass_must_block_teaching(self) -> None:
        with self.make_root() as directory:
            root = Path(directory)
            handoff, _ = build_handoff(root, status="blocked", reviews=[("unavailable", "reviewer-one")])
            self.assertTrue(validate_handoff(handoff, repo_root=root).ok)
            self.assert_code(validate_handoff(handoff, repo_root=root, ready=True), "REVIEW_NOT_PASS")

            handoff, _ = build_handoff(
                root,
                status="blocked",
                reviews=[("changes_required", "reviewer-one"), ("changes_required", "reviewer-two")],
            )
            self.assertTrue(validate_handoff(handoff, repo_root=root).ok)
            self.assert_code(validate_handoff(handoff, repo_root=root, ready=True), "REVIEW_NOT_PASS")

    def test_source_mutation_and_contract_mutation_are_detected(self) -> None:
        with self.make_root() as directory:
            root = Path(directory)
            handoff, _ = build_handoff(root, status="active", reviews=[("pass", "fresh-reviewer")])
            (root / "materials/lesson.md").write_text("changed", encoding="utf-8")
            source_report = validate_handoff(handoff, repo_root=root)
            self.assert_code(source_report, "SOURCE_HASH")
            self.assert_code(source_report, "REVIEW_STALE")

            handoff, _ = build_handoff(root, status="active", reviews=[("pass", "fresh-reviewer")], primary_bytes=b"changed")
            changed_contract = handoff.read_text(encoding="utf-8").replace(
                "Trace a tensor operation", "Trace one tensor operation"
            )
            handoff.write_text(changed_contract, encoding="utf-8")
            contract_report = validate_handoff(handoff, repo_root=root)
            self.assert_code(contract_report, "CONTRACT_HASH")
            self.assert_code(contract_report, "REVIEW_STALE")

    def test_review_attempt_count_cannot_exceed_two(self) -> None:
        with self.make_root() as directory:
            root = Path(directory)
            handoff, _ = build_handoff(
                root,
                status="blocked",
                reviews=[
                    ("changes_required", "reviewer-one"),
                    ("changes_required", "reviewer-two"),
                    ("pass", "reviewer-three"),
                ],
            )
            report = validate_handoff(handoff, repo_root=root)
            self.assertFalse(report.ok)
            self.assertEqual(report.exit_code, 2)
            self.assert_code(report, "SCHEMA")

    def test_parent_traversal_and_external_symlink_are_rejected(self) -> None:
        with self.make_root() as directory, self.make_root() as outside_directory:
            root = Path(directory)
            handoff, _ = build_handoff(root)
            text = handoff.read_text(encoding="utf-8").replace("materials/lesson.md", "../lesson.md")
            handoff.write_text(text, encoding="utf-8")
            self.assert_code(validate_handoff(handoff, repo_root=root), "PATH")

            root = Path(directory) / "second"
            external = Path(outside_directory) / "external.md"
            external.write_text("outside", encoding="utf-8")
            (root / "materials").mkdir(parents=True)
            os.symlink(external, root / "materials/link.md")
            handoff, _ = build_handoff(root, primary_path="materials/link.md")
            self.assert_code(validate_handoff(handoff, repo_root=root), "PATH")

    def test_curriculum_role_requires_canonical_path_and_target_membership(self) -> None:
        with self.make_root() as directory:
            root = Path(directory)
            handoff, _ = build_handoff(root)
            text = handoff.read_text(encoding="utf-8").replace(
                "| I002 | curriculum | CURRICULUM.md |", "| I002 | curriculum | materials/lesson.md |"
            )
            handoff.write_text(text, encoding="utf-8")
            self.assert_code(validate_handoff(handoff, repo_root=root), "PATH")

            handoff, _ = build_handoff(root)
            (root / "CURRICULUM.md").write_text("# Curriculum without the target\n", encoding="utf-8")
            # Rebuild so the manifest hash is current; only curriculum alignment should fail.
            handoff, _ = build_handoff(root)
            report = validate_handoff(handoff, repo_root=root)
            self.assert_code(report, "REVIEW_NOT_PASS")

    def test_concept_source_path_must_be_manifested(self) -> None:
        with self.make_root() as directory:
            root = Path(directory)
            handoff, _ = build_handoff(root)
            text = handoff.read_text(encoding="utf-8").replace(
                "materials/lesson.md#shape-propagation", "materials/unreviewed.md#shape-propagation"
            )
            # Keep the declared contract hash current so this isolates manifest alignment.
            start = text.index("<!-- lesson-contract:start -->") + len("<!-- lesson-contract:start -->\n")
            end = text.index("\n<!-- lesson-contract:end -->")
            text = re_sub_field(text, "contract_sha256", sha256(text[start:end]))
            handoff.write_text(text, encoding="utf-8")
            self.assert_code(validate_handoff(handoff, repo_root=root), "REVIEW_NOT_PASS")

    def test_mutable_draft_cannot_be_a_manifest_input(self) -> None:
        with self.make_root() as directory:
            root = Path(directory)
            handoff, hashes = build_handoff(root)
            draft = root / "til/today.md"
            draft.parent.mkdir(parents=True)
            draft.write_text("learner scratch\n", encoding="utf-8")
            text = handoff.read_text(encoding="utf-8")
            draft_hash = sha256(draft.read_bytes())
            text = text.replace(
                "<!-- lesson-contract:start -->",
                f"| I003 | til | til/today.md | {draft_hash} |\n\n<!-- lesson-contract:start -->",
                1,
            )
            manifest_hash = sha256(
                "".join(
                    sorted(
                        [
                            f"primary\tmaterials/lesson.md\t{sha256((root / 'materials/lesson.md').read_bytes())}\n",
                            f"curriculum\tCURRICULUM.md\t{sha256((root / 'CURRICULUM.md').read_bytes())}\n",
                            f"til\ttil/today.md\t{draft_hash}\n",
                        ]
                    )
                )
            )
            text = re_sub_field(text, "input_manifest_sha256", manifest_hash)
            handoff.write_text(text, encoding="utf-8")
            report = validate_handoff(handoff, repo_root=root)
            self.assert_code(report, "PATH")

    def test_evidence_state_and_content_hash_are_checked(self) -> None:
        with self.make_root() as directory:
            root = Path(directory)
            handoff, _ = build_handoff(
                root,
                status="active",
                reviews=[("pass", "fresh-reviewer")],
                evidence=[{"verdict": "partial", "append_state": "pending"}],
            )
            self.assert_code(validate_handoff(handoff, repo_root=root), "EVIDENCE_STATE")
            handoff, _ = build_handoff(
                root,
                status="active",
                reviews=[("pass", "fresh-reviewer")],
                evidence=[{"verdict": "confirmed", "append_state": "pending"}],
            )
            text = handoff.read_text(encoding="utf-8").replace("배치 축과 특성 축", "배치 축과 시간 축")
            handoff.write_text(text, encoding="utf-8")
            self.assert_code(validate_handoff(handoff, repo_root=root), "EVIDENCE_STATE")

    def test_materialized_untouched_preparing_template_has_no_phantom_blocks(self) -> None:
        with self.make_root() as directory:
            root = Path(directory)
            (root / "materials").mkdir(parents=True)
            source = root / "materials/lesson.md"
            curriculum = root / "CURRICULUM.md"
            source.write_text("# source\n", encoding="utf-8")
            curriculum.write_text("# curriculum\n\n## CC-DL-01\n", encoding="utf-8")
            source_hash = sha256(source.read_bytes())
            curriculum_hash = sha256(curriculum.read_bytes())
            template = (SKILL / "assets/active-lesson-handoff-template.md").read_text(encoding="utf-8")
            raw_path = root / "tmp/raw-template.md"
            raw_path.parent.mkdir(parents=True)
            raw_path.write_text(template, encoding="utf-8")
            self.assertFalse(validate_handoff(raw_path, repo_root=root).ok)

            text = template.replace("replace-with-stable-lesson-id", "template-lesson")
            text = text.replace("YYYY-MM-DDTHH:MM:SSZ", "2026-08-20T00:00:00Z")
            text = text.replace("YYYY-MM-DD", "2026-08-20")
            text = text.replace("materials/private/course/NN-NN_lesson.md", "materials/lesson.md")
            text = text.replace(
                "| I001 | primary | materials/lesson.md | replace-with-file-sha256 |",
                f"| I001 | primary | materials/lesson.md | {source_hash} |",
            )
            text = text.replace(
                "| I002 | curriculum | CURRICULUM.md | replace-with-file-sha256 |",
                f"| I002 | curriculum | CURRICULUM.md | {curriculum_hash} |",
            )
            manifest_hash = sha256(
                "".join(
                    sorted(
                        [
                            f"primary\tmaterials/lesson.md\t{source_hash}\n",
                            f"curriculum\tCURRICULUM.md\t{curriculum_hash}\n",
                        ]
                    )
                )
            )
            start = text.index("<!-- lesson-contract:start -->") + len("<!-- lesson-contract:start -->\n")
            end = text.index("\n<!-- lesson-contract:end -->")
            contract_hash = hashlib.sha256(text[start:end].encode("utf-8")).hexdigest()
            text = text.replace("replace-with-64-lowercase-hex", manifest_hash, 1)
            text = text.replace("replace-with-64-lowercase-hex", contract_hash, 1)
            ready_path = root / "tmp/active-lesson-handoff.md"
            ready_path.write_text(text, encoding="utf-8")
            report = validate_handoff(ready_path, repo_root=root)
            self.assertTrue(report.ok, report.errors)
            self.assertEqual(report.document.review_attempt_count, 0)
            self.assertEqual(report.document.evidence, {})

    def test_json_cli_and_error_format(self) -> None:
        (REPO / "tmp").mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=REPO / "tmp") as directory:
            root = Path(directory)
            handoff, _ = build_handoff(root)
            relative_directory = root.relative_to(REPO)
            text = handoff.read_text(encoding="utf-8")
            text = text.replace("materials/lesson.md", f"{relative_directory.as_posix()}/materials/lesson.md")
            source_hash = sha256((root / "materials/lesson.md").read_bytes())
            curriculum_hash = sha256((REPO / "CURRICULUM.md").read_bytes())
            import re

            text = re.sub(
                r"\| I002 \| curriculum \| CURRICULUM\.md \| [0-9a-f]{64} \|",
                f"| I002 | curriculum | CURRICULUM.md | {curriculum_hash} |",
                text,
                count=1,
            )
            manifest_hash = sha256(
                "".join(
                    sorted(
                        [
                            f"primary\t{relative_directory.as_posix()}/materials/lesson.md\t{source_hash}\n",
                            f"curriculum\tCURRICULUM.md\t{curriculum_hash}\n",
                        ]
                    )
                )
            )
            # Both source-location text and manifest paths changed. Recompute only the
            # declared hashes; the preparing template needs no semantic review.
            contract_start = text.index("<!-- lesson-contract:start -->") + len("<!-- lesson-contract:start -->\n")
            contract_end = text.index("\n<!-- lesson-contract:end -->")
            contract_hash = sha256(text[contract_start:contract_end])
            text = re_sub_field(text, "input_manifest_sha256", manifest_hash)
            text = re_sub_field(text, "contract_sha256", contract_hash)
            handoff.write_text(text, encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(SKILL / "scripts/validate_lesson_handoff.py"), "--json", handoff.relative_to(REPO).as_posix()],
                cwd=REPO,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            payload = json.loads(result.stdout)
            self.assertTrue(payload["ok"])

    def test_cli_usage_error_uses_validator_error_contract(self) -> None:
        result = subprocess.run(
            [sys.executable, str(SKILL / "scripts/validate_lesson_handoff.py")],
            cwd=REPO,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertRegex(
            result.stderr,
            r"^ERROR <cli>:1 \[SCHEMA\] the following arguments are required: handoff\n$",
        )

        conflict = subprocess.run(
            [
                sys.executable,
                str(SKILL / "scripts/validate_lesson_handoff.py"),
                "--ready",
                "--til-ready",
                "tmp/active-lesson-handoff.md",
            ],
            cwd=REPO,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(conflict.returncode, 2)
        self.assertEqual(conflict.stdout, "")
        self.assertRegex(conflict.stderr, r"^ERROR <cli>:1 \[SCHEMA\] argument --til-ready: not allowed with argument --ready\n$")


def re_sub_field(text: str, key: str, value: str) -> str:
    import re

    return re.sub(rf"^- {re.escape(key)}: .*$", f"- {key}: {value}", text, count=1, flags=re.MULTILINE)


if __name__ == "__main__":
    unittest.main()
