#!/usr/bin/env python3
"""Build `manifest.json` from the plugin manifests listed in `sources.json`.

Every package is written out in the feed, in the order of `sources.json`. A
plugin whose manifest cannot be fetched keeps its packages from the current
`manifest.json`, so one unreachable repository does not drop it. The file is
only rewritten when its content changes.

    build_feed.py           build manifest.json next to sources.json
"""

import json
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCES = ROOT / "sources.json"
FEED = ROOT / "manifest.json"
TIMEOUT_SECONDS = 30


def fetch(url):
    request = urllib.request.Request(url, headers={"Accept": "application/json", "User-Agent": "shoko-plugin-feed"})
    with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
        return json.load(response)


def packages_of(document):
    """The packages of a manifest: one package or a list of them. An entry
    without an ID, a name or releases is left out."""
    entries = document if isinstance(document, list) else [document]
    return [
        entry for entry in entries
        if isinstance(entry, dict)
        and isinstance(entry.get("id"), str)
        and isinstance(entry.get("name"), str)
        and isinstance(entry.get("releases"), list)
    ]


def main():
    sources = json.loads(SOURCES.read_text(encoding="utf-8"))
    previous = packages_of(json.loads(FEED.read_text(encoding="utf-8"))) if FEED.exists() else []
    previous_by_id = {}
    for package in previous:
        previous_by_id.setdefault(package["id"].lower(), []).append(package)

    feed = []
    for source in sources:
        package_id, url = source["id"].lower(), source["url"]
        try:
            packages = packages_of(fetch(url))
            if not any(package["id"].lower() == package_id for package in packages):
                raise ValueError(f"no package {package_id}")
            feed.extend(packages)
        except Exception as error:  # noqa: BLE001 - any failure falls back to the last good copy
            kept = previous_by_id.get(package_id, [])
            print(f"::warning::{url}: {error}; {'kept the last good copy' if kept else 'left out, with no earlier copy'}.", file=sys.stderr)
            feed.extend(kept)

    if sources and not feed:
        sys.exit("No manifest could be read; leaving manifest.json as it is.")

    content = json.dumps(feed, indent=2, ensure_ascii=False) + "\n"
    if FEED.exists() and FEED.read_text(encoding="utf-8") == content:
        print("manifest.json is unchanged.")
        return

    FEED.write_text(content, encoding="utf-8")
    print(f"manifest.json now lists {len(feed)} packages.")


if __name__ == "__main__":
    main()
