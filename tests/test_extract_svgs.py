import zipfile

import pytest

from kanji_stroke_order.build import extract_svgs


def _archive(tmp_path, names):
    archive = tmp_path / "kanjivg-all.zip"
    with zipfile.ZipFile(archive, "w") as zipf:
        for name in names:
            zipf.writestr(name, name)
    return archive


def test_extracts_svgs_flat_and_sorted(tmp_path):
    archive = _archive(tmp_path, ["kanji/05b57.svg", "kanji/04e00.svg", "README.md"])
    svgs = extract_svgs(archive, tmp_path / "svgs")
    assert list(svgs) == ["04e00.svg", "05b57.svg"]
    assert svgs["05b57.svg"].read_text() == "kanji/05b57.svg"


def test_fails_on_duplicate_file_names(tmp_path):
    with pytest.raises(ValueError, match="more than one"):
        extract_svgs(_archive(tmp_path, ["a/04e00.svg", "b/04e00.svg"]), tmp_path / "svgs")
