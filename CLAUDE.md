# CLAUDE.md

## Workflow preferences

- **Git:** You may run read-only git commands that don't change the repository, its
  history, or its remotes without asking (for example, `git status`, `git log`,
  `git diff`, `git show`, `git branch` with no arguments or with `--show-current`, and
  `git blame`). Always ask me to manually approve every other git command, including
  anything that commits, stages, checks out, merges, rebases, resets, stashes, fetches,
  pulls, pushes, or creates or deletes branches or tags.
- **Planning:** Plan first and get my approval before making any large changes.
- **Test-driven development:** Write tests first, then the code that makes them pass.
- **Debugging:** Debug with print statements and tests first.
- **Contributing guide:** Follow [CONTRIBUTING.md](CONTRIBUTING.md) for branching, commit messages,
  pull requests, testing, and documentation. Where it conflicts with these preferences, default to [CONTRIBUTING.md](CONTRIBUTING.md) and ask me if more details are required.
- **AI usage log:** At the end of any task where you wrote, debugged, refactored, or reviewed
  code, or found or explained outside resources, use the `ai-log`
  skill to update [AI_USAGE.md](AI_USAGE.md). Summarize the general task in a sentence, do not explain every step.

### 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

### 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

### 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it - don't delete it.

When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.

### 4. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:
- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:
```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

### These guidelines are working if:

1. fewer unnecessary changes in diffs, 
2. fewer rewrites due to overcomplication, and 
3. clarifying questions come before implementation rather than after mistakes.

## Scientific & Astronomical Software Development

Some guidelines that we must follow when building this scientifc software:
1. Always check for a wrapping error when doing anything with right ascension (RA)
2. Magnitudes are tricky, but astronomers love them. Be careful when handling magnitudes.
3. Sources must be cited. You can include this with DOIs in docstrings.

## Code style

- Follow the [astropy](https://github.com/astropy/astropy) codebase as the reference for code style and documentation.
- Follow the PEP 8 style guide for Python.
- Use Google-style docstrings.
- Write code as simply as possible.
- Use descriptive variable, class, and function names, as long as they aren't too long.
- Make code reusable within the codebase, and reuse existing code before rewriting anything.

## Project overview

`convert_flux` is a Python package (alexander-group, University of Arizona) for converting
between astronomical magnitudes, flux densities, fluxes, and luminosities. It is built on
`astropy.units`: all inputs and outputs are `astropy` Quantities. Status: pre-alpha.

## Architecture

```
convert_flux/
├── convert_flux.py          # Public entry point: convert_flux()
├── brightness_models/       # One class per brightness quantity
│   ├── flux.py              # Flux
│   ├── fluxdensity.py       # FluxDensity
│   ├── luminosity.py        # Luminosity
│   └── magnitude.py         # Mag
├── converters/              # One class per pair of quantities
│   ├── fluxfluxdensity.py   # FluxFluxDensity
│   ├── fluxluminosity.py    # FluxLuminosity
│   └── magfluxdensity.py    # MagFluxDensity
└── utils/                   # Supporting units, spectra, and transmission curves
    ├── convert_flux_units.py    # Custom units (VEGAMAG)
    ├── source_spec_models.py    # Source spectrum shapes (SourceSpec ABC, FlatSpec, ...)
    └── transmission.py          # TransmissionCurve (placeholder)
```

Everything in `utils/` is re-exported from `convert_flux/utils/__init__.py`, so import it as
`from ..utils import VEGAMAG, FlatSpec` (or `from convert_flux.utils import ...` in tests).

### Brightness models (`brightness_models/`)

Each class wraps an `astropy` Quantity. It checks the input type (and raises `TypeError` if
it isn't a Quantity) and converts the value to a standard internal unit stored in `.quantity`:

| Class | Constructor | Internal unit |
|---|---|---|
| `Flux` | `Flux(quantity)` | erg / (s cm²) |
| `FluxDensity` | `FluxDensity(quantity, spectral_coordinate)` | erg / (s cm² Å); `spectral_coordinate` stored in Å |
| `Luminosity` | `Luminosity(quantity)` | erg / s |
| `Mag` | `Mag(quantity, spectral_coordinate, chosen_mag_system=None)` | ABmag by default; accepts ABmag, STmag, VEGAMAG |

Vega magnitude handling in `Mag` is unfinished: it returns early and sets no `.quantity`.
It is waiting on the source spectrum work.

### Converters (`converters/`)

Each converter takes brightness model objects and returns brightness model objects. Conversions
always go through the internal units.

- `FluxLuminosity(flux=None, luminosity=None, cosmo=Planck18)`: `flux_to_luminosity(distance=None, z=None)`
  and `luminosity_to_flux(...)` use L = 4πd²F. If `z` is given, the luminosity distance comes
  from `cosmo`.
- `FluxFluxDensity(flux=None, flux_density=None)`: `flux_to_fluxdensity(transmission, wavelength, source_spec=None)`
  and `flux_density_to_flux(...)` integrate (`scipy.integrate.trapezoid`) over the transmission
  curve weighted by the source spectrum shape. The default source spectrum is `FlatSpec`.
- `MagFluxDensity(mag=None, flux_density=None, spectral_coordinate=None)`: `mag_to_flux_density(spectral_coordinate)`
  and `flux_density_to_mag(...)` use astropy's `spectral_density` equivalency. Raw Quantities are
  wrapped into `Mag` / `FluxDensity` automatically.

### Source spectra and transmission

- `SourceSpec` (ABC): `shape(wavelength)` validates the input (it must be a Quantity), converts it
  to Å, and calls the subclass's `_shape()`. It returns a dimensionless array on the same grid as
  the transmission curve.
- `FlatSpec` is implemented. `LymASpec` (Lyman alpha break) and `PolySpec` are empty stubs.
- `TransmissionCurve` is a placeholder. It will eventually use the `infer_filter_info` package.
  A flat curve should be something the user explicitly chooses, not a default.

### Public API: `convert_flux()` (in progress)

`convert_flux(input_quantity, output_unit, source_spec_shape=None, transmission_curve=None)`
is the single user-facing function (exported in `__init__.py`). It is currently a stub that
returns `None`. It is meant to detect the input and output quantity types, wrap them in
brightness models, and chain the converters (for example, mag → flux density → flux →
luminosity). This is the work on branch `28-write-the-convert_flux-function`.

## Units

The supported and default units are documented in [docs/conversion_units.rst](docs/conversion_units.rst).
Default user-facing units: AB mag, erg/(s cm²) for flux, uJy (frequency) or erg/(s cm² Å)
(wavelength) for flux density, and erg/s for luminosity.

## Dependencies

- Keep the package's dependencies to an absolute minimum so it is as easy as possible
  for users to install and use. Don't add a new dependency without asking me first.
- Don't make `synphot` a dependency. It is fine to adapt parts of
  `synphot.units.convert_flux()` (and related helpers) into this package, as long as
  synphot gets credit:
  - Add a comment or docstring note on the adapted code naming its source, for example
    "Adapted from synphot.units.convert_flux (STScI, BSD 3-Clause License)".
  - synphot is BSD 3-Clause licensed (Copyright (c) Space Telescope Science Institute,
    AURA). Keep its copyright notice and license text with the adapted code, for
    example in a `licenses/SYNPHOT_LICENSE.rst` file.
  - Mention synphot in the docs (for example, an acknowledgements or references section).

## Development

Use an environment for running code and tests:

- Python ≥ 3.9. CI tests 3.10 and 3.11 on Ubuntu and macOS, with coverage uploaded to Codecov.
- Ruff: line length 88, rules E/F/N/W, `E712` ignored, `__init__.py` excluded, double quotes.
- Dependencies: `numpy`, `astropy>=6`, `scipy>=1.14`, `infer_filter_info`.

## Tests (`tests/`)

- `test_<name>_class.py`: unit tests for each brightness model and converter. Real filter
  wavelengths (SDSS, ZTF) are used in `pytest.mark.parametrize` with `ids`.
- `test_unit_*.py`: end-to-end tests for `convert_flux()`. They are marked
  `@pytest.mark.xfail` until the function is implemented. Remove the `xfail` marker once a
  test passes.
- Tests check values with a relative tolerance, for example `abs(actual - expected) / expected <= 1e-3`.

## Commits and releases

Releases are automated with `python-semantic-release` when changes are pushed to `main`.
Commit messages must use conventional commit tags:

- `feat:` for a minor version bump.
- `fix:` or `perf:` for a patch bump.
- `build`, `chore`, `ci`, `docs`, `style`, `refactor`, `test` for no release.

Use the present tense and the imperative mood, and keep the first line to 72 characters or
fewer. The version is stored in `convert_flux/_version.py`.
