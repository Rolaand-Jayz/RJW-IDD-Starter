import pathlib

from validate_ids_video_addin import validate_files


def test_validate_ids_pass(tmp_path: pathlib.Path):
    file_path = tmp_path / "doc.md"
    file_path.write_text("SPEC-VIDEO-QA-0001 and DOC-VIDEO-GUIDE-0005")
    errors = validate_files([file_path])
    assert errors == []


def test_validate_ids_rejects_prefix(tmp_path: pathlib.Path):
    file_path = tmp_path / "bad.txt"
    file_path.write_text("BAD-" + "VIDEO-0001")
    errors = validate_files([file_path])
    assert errors
