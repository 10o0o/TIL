from __future__ import annotations

import hashlib
import importlib.util
import unittest
from pathlib import Path


SCRIPT = (
    Path(__file__).resolve().parents[1]
    / "scripts"
    / "strip_lesson_evidence_markers.py"
)
SPEC = importlib.util.spec_from_file_location("strip_lesson_evidence_markers", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def envelope(content: str, *, digest: str | None = None) -> str:
    content_digest = digest or hashlib.sha256(content.encode("utf-8")).hexdigest()
    return (
        f"<!-- lesson-evidence:lesson-one:E001:{content_digest} -->\n"
        f"{content}\n"
        "<!-- /lesson-evidence:lesson-one:E001 -->\n"
    )


class StripMarkersTests(unittest.TestCase):
    def test_draft_without_markers_is_byte_for_byte_unchanged(self) -> None:
        draft = "# 메모\r\n\r\n학습자 문장\r\n"
        self.assertEqual(MODULE.strip_markers(draft), draft)

    def test_valid_envelope_removes_only_comments(self) -> None:
        content = "내가 직접 설명한 내용\n두 번째 줄"
        draft = f"앞 문단\n\n{envelope(content)}\n뒤 문단\n"
        self.assertEqual(
            MODULE.strip_markers(draft),
            f"앞 문단\n\n{content}\n\n뒤 문단\n",
        )

    def test_content_leading_and_trailing_lf_are_preserved(self) -> None:
        content = "\n학습자 답변\n"
        self.assertEqual(MODULE.strip_markers(envelope(content)), content + "\n")

    def test_marker_body_uses_lf_normalized_hash(self) -> None:
        content = "첫 줄\n둘째 줄"
        draft = envelope(content).replace("\n", "\r\n")
        self.assertEqual(MODULE.strip_markers(draft), content + "\n")

    def test_following_paragraph_is_not_concatenated(self) -> None:
        content = "학습자 답변"
        draft = envelope(content) + "바로 이어지는 문단\n"
        self.assertEqual(
            MODULE.strip_markers(draft),
            content + "\n바로 이어지는 문단\n",
        )

    def test_hash_mismatch_is_rejected(self) -> None:
        draft = envelope("학습자 답변", digest="0" * 64)
        with self.assertRaisesRegex(MODULE.MarkerError, "SHA-256 mismatch"):
            MODULE.strip_markers(draft)

    def test_mismatched_close_is_rejected(self) -> None:
        content = "학습자 답변"
        digest = hashlib.sha256(content.encode("utf-8")).hexdigest()
        draft = (
            f"<!-- lesson-evidence:lesson-one:E001:{digest} -->\n"
            f"{content}\n"
            "<!-- /lesson-evidence:lesson-one:E002 -->\n"
        )
        with self.assertRaisesRegex(MODULE.MarkerError, "does not match"):
            MODULE.strip_markers(draft)

    def test_duplicate_envelope_is_rejected(self) -> None:
        draft = envelope("학습자 답변") * 2
        with self.assertRaisesRegex(MODULE.MarkerError, "duplicate evidence envelope"):
            MODULE.strip_markers(draft)


if __name__ == "__main__":
    unittest.main()
