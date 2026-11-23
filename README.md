# kanji-stroke-order-dakanji

Kanji stroke order (KanjiVG) for DaKanji.

The dictionary is in the `dakanji-stroke-order` format: an `index.json` and one KanjiVG `.svg` per character and variant.
DaKanji's database build downloads it as `kanjivg-dadb.zip`, so the asset keeps that name.

## Sources

* [KanjiVG](https://github.com/KanjiVG/kanjivg) by Ulrich Apel: every SVG of its `kanjivg-*-all.zip` release asset, unchanged,
  locked to a release in `sources.lock.json`.

## Installation

Make sure [uv](https://github.com/astral-sh/uv) is installed on your system and run

``` bash
uv sync
```

## Usage

``` bash
uv run build.py
```

This creates `out/kanjivg-dadb.zip` with its `.index.json` and `.manifest.json`.
Downloaded sources are cached in `tmp/sources/`, the SVGs are extracted to `tmp/kanjivg/`.

## Development

``` bash
uv run ruff check .          # lint
uv run ruff format .         # format
uv run pyright               # type check
uv run pytest                # tests
```

The repo follows the [DaLang dictionary repo standard](https://github.com/dariyooo/dalang-dict-utils/blob/main/docs/repo-standard.md),
update the shared setup with `uvx copier update --trust`.

## Release

Push a tag with today's date:

``` bash
git tag 2026-11-23 && git push origin 2026-11-23
```

The *Release* workflow runs the checks, builds with the tag as revision and publishes the GitHub release of the tag.
To redo a release, push the tag again with `git tag -f 2026-11-23 && git push -f origin 2026-11-23`.
The *Update* workflow checks the sources weekly and releases on its own if the output changed.

## License

KanjiVG © Ulrich Apel and contributors, [CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/).
