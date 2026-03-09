# CHANGELOG

The format is based on [Keep a Changelog](https://keepachangelog.com/), and this project adheres to [Semantic Versioning](https://semver.org/).
<!--
    Test that your file format adheres adequetely to the Keep A Changelog standard by pasting this changelog content into the test string field here: https://regex101.com/r/8JROUv/1
    Consequences of having an improperly-formatted changelog: The qgis-plugin-ci tool relies on this changelog formatting to pick the latest version number when packaging the plugin and producing metadata. If the changelog is incorrectly formatted, the version listed with your package will be incorrect.
-->
<!--

Unreleased

## version_tag - YYYY-DD-mm

### Added

### Changed

### Removed

-->

## 1.0.1 - 2026-01-03

Release 1.0.1 bumps tooling dependencies and fixes UI labeling.

### Tooling 🔧
* Bump actions/upload-artifact from 6 to 7 by @dependabot[bot] in https://github.com/alxwstn/RAFTHeatmapMkr/pull/23
* Bump dawidd6/action-download-artifact from 9 to 16 by @dependabot[bot] in https://github.com/alxwstn/RAFTHeatmapMkr/pull/22
* Bump actions/download-artifact from 7 to 8 by @dependabot[bot] in https://github.com/alxwstn/RAFTHeatmapMkr/pull/19
* Bump actions/checkout from 4 to 6 by @dependabot[bot] in https://github.com/alxwstn/RAFTHeatmapMkr/pull/21
* Bump actions/setup-python from 5 to 6 by @dependabot[bot] in https://github.com/alxwstn/RAFTHeatmapMkr/pull/20
### Other Changes
* fix settings menu label by @alxwstn in https://github.com/alxwstn/RAFTHeatmapMkr/pull/24

## 1.0.0 - 2026-29-02

Release 1.0.0 refactors the UI to improve usability, improves layer styling, bumps dependencies, and improves documentation.

### Features and enhancements 🎉
* UI improvements by @alxwstn in https://github.com/alxwstn/RAFTHeatmapMkr/pull/9
### Tooling 🔧
* Bump actions/labeler from 5 to 6 by @dependabot[bot] in https://github.com/alxwstn/RAFTHeatmapMkr/pull/5
* Bump actions/cache from 4 to 5 by @dependabot[bot] in https://github.com/alxwstn/RAFTHeatmapMkr/pull/4
* Bump actions/download-artifact from 4 to 7 by @dependabot[bot] in https://github.com/alxwstn/RAFTHeatmapMkr/pull/3
* Bump actions/upload-pages-artifact from 3 to 4 by @dependabot[bot] in https://github.com/alxwstn/RAFTHeatmapMkr/pull/2
* Bump actions/upload-artifact from 4 to 6 by @dependabot[bot] in https://github.com/alxwstn/RAFTHeatmapMkr/pull/1
### Documentation 📖
* update install doc and fix doc root config by @alxwstn in https://github.com/alxwstn/RAFTHeatmapMkr/pull/6
* Docs by @alxwstn in https://github.com/alxwstn/RAFTHeatmapMkr/pull/11
### Other Changes
* Update icon by @alxwstn in https://github.com/alxwstn/RAFTHeatmapMkr/pull/7
* Bugfix plugin dependencies by @alxwstn in https://github.com/alxwstn/RAFTHeatmapMkr/pull/8

## 0.1.0 - 2026-21-02

- Development release
- Configure heatmap Proof of Concept plugin code.
- Initial framework generated with the [QGIS Plugins templater](https://oslandia.gitlab.io/qgis/template-qgis-plugin/)
