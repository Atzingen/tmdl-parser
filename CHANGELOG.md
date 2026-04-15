# Changelog

## v0.2.0

### Added
- `TMLDParser.to_dict()` — return the parsed structure as a nested Python dictionary.
- `TMLDParser.to_dataframe(flatten=True)` — return the parsed structure as a pandas `DataFrame`. Pandas is an optional dependency, installable via `pip install tmdl-parser[pandas]`.
- `TMDL.to_dict()` — recursive conversion helper on the dataclass itself.
- First test suite under `tests/` covering the new export APIs.

### Changed
- `save_to_json()` now delegates to `to_dict()` internally (no duplication).

## v1.0.0

### Added or Changed
- Added this changelog :)
- Fixed typos in both templates
- Back to top links
- Added more "Built With" frameworks/libraries
- Changed table of contents to start collapsed
- Added checkboxes for major features on roadmap

### Removed

- Some packages/libraries from acknowledgements I no longer use