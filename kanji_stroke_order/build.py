import shutil
import zipfile
from pathlib import Path, PurePosixPath

from dalang_dict import GitHubReleaseAsset, build_index, fetch, package_dictionary

GITHUB_REPO = "dariyooo/kanji-stroke-order-dakanji"
# DaKanji's database build downloads `kanjivg-dadb.zip`, so the asset keeps its name
ASSET = "kanjivg-dadb"
TITLE = "KanjiVG"
SVG_DIR = Path("tmp/kanjivg")

# Locked to a KanjiVG release in sources.lock.json, updated by the Update workflow.
# The asset name contains the release date, e.g. `kanjivg-20260714-all.zip`.
KANJIVG = GitHubReleaseAsset(
    "kanjivg-all.zip",
    repo="KanjiVG/kanjivg",
    asset="kanjivg-*-all.zip",
    used_for="stroke order SVGs of every character and its variants",
)

INDEX_FIELDS = {
    "sourceLanguage": "ja",
    "author": "Ulrich Apel (KanjiVG)",
    "url": f"https://github.com/{GITHUB_REPO}",
    "description": "Stroke order of the kanji and kana from KanjiVG for DaKanji.",
    "attribution": "KanjiVG © Ulrich Apel and contributors, CC BY-SA 3.0.",
}


def extract_svgs(archive: Path, target: Path) -> dict[str, Path]:
    """Extracts the SVG files of a KanjiVG release into `target`, returns them by file name."""
    shutil.rmtree(target, ignore_errors=True)
    target.mkdir(parents=True)
    svgs = {}
    with zipfile.ZipFile(archive) as zipf:
        for name in zipf.namelist():
            file_name = PurePosixPath(name).name
            if not file_name.endswith(".svg"):
                continue
            if file_name in svgs:
                raise ValueError(f"'{archive}' has more than one '{file_name}'")
            svgs[file_name] = target / file_name
            svgs[file_name].write_bytes(zipf.read(name))
    return dict(sorted(svgs.items()))


def main() -> None:
    svgs = extract_svgs(fetch(KANJIVG), SVG_DIR)

    index = build_index(TITLE, GITHUB_REPO, ASSET, **INDEX_FIELDS)
    package_dictionary(ASSET, index, {}, extra_files=svgs, format="dakanji-stroke-order")
