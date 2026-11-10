# Shoko Plugin Manifest

Aggregate manifest for all Shoko plugins by revam.

## Usage

Add this manifest URL to your Shoko server under **Settings → Plugins → Repositories**:

```
https://raw.githubusercontent.com/revam/dotnet-shoko-plugin-manifest/metadata/manifest.json
```

This will automatically include all available plugins:

| Plugin | Description |
|--------|-------------|
| [AnimeSchedule.net](https://github.com/revam/dotnet-shoko-plugin-animeschedule) | Airing schedules, delays and streaming links from AnimeSchedule.net |
| [Fanart.tv Artwork](https://github.com/revam/dotnet-shoko-plugin-fanart) | Series and movie artwork from Fanart.tv for TMDb and TheTVDB entries |
| [Release Importer/Exporter](https://github.com/revam/dotnet-shoko-plugin-release-exporter) | Import/export releases from filesystem |
| [Release Retry](https://github.com/revam/dotnet-shoko-plugin-release-retry) | Re-attempt release searches after failure |
| [Relocation+](https://github.com/revam/dotnet-shoko-plugin-relocation-plus) | Relocate video extra files near video files |
| [Syoboi Calendar](https://github.com/revam/dotnet-shoko-plugin-syoboi) | Japanese TV and streaming broadcast schedules from cal.syoboi.jp |
| [TvDB](https://github.com/revam/dotnet-shoko-plugin-tvdb) | Series metadata, images, cast and alternate orderings from TheTVDB |
| [TVmaze Airing Schedule](https://github.com/revam/dotnet-shoko-plugin-tvmaze) | Airing schedules from TVmaze for TMDB-linked shows |

## How the feed is built

`sources.json` lists each plugin's own manifest. `scripts/build_feed.py`
fetches them and writes `manifest.json` with every package written out, in
that order; a plugin whose manifest cannot be fetched keeps its packages
from the previous build. The **Build the feed** workflow runs it every hour,
by hand, and when the list changes, and commits `manifest.json` only when it
changed, so a release shows up within the hour. Adding a plugin is one entry
in `sources.json`, when it first releases.

## License

This project is licensed under the MIT License.
