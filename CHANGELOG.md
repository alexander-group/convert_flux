# CHANGELOG

<!-- version list -->

## v0.3.0 (2026-11-20)

### Bug Fixes

- Restore mean wavelength in TransmissionCurve.from_filter
  ([`1b129e8`](https://github.com/alexander-group/convert_flux/commit/1b129e85db05a90d14af7c54cbe73c1b3d07fc7d))

### Build System

- Fix unit tests that were prev xfail. update convert_flux to work with infer_filter_info
  inputs/outputs.
  ([`05003f2`](https://github.com/alexander-group/convert_flux/commit/05003f2bfb85cd41ad1b354376d0e7c92ce37408))

### Documentation

- Info about ai-log skill
  ([`7bcbc4b`](https://github.com/alexander-group/convert_flux/commit/7bcbc4b592413ba2088b63caa58eef389d75f085))

- Log AI contributions
  ([`3c16cc3`](https://github.com/alexander-group/convert_flux/commit/3c16cc3949454c8e1215176090a02832b9abed6e))

- Update supported units documentation
  ([`c164e0a`](https://github.com/alexander-group/convert_flux/commit/c164e0a1fe7472128c9df65e2d97e33a723f0147))

### Features

- Implement convert_flux function using existing converters and brightness models
  ([`731320f`](https://github.com/alexander-group/convert_flux/commit/731320f878132d2a82bdfb7e7d6e30a248382f4d))

### Testing

- Update unit test to use non-approx transmission curve value
  ([`7cfa7b5`](https://github.com/alexander-group/convert_flux/commit/7cfa7b525b4023aa8f1172dfb9e51cb968277b00))


## v0.2.1 (2026-11-19)

### Bug Fixes

- Added default of perfect transmission that user can lower if needed
  ([`b0098f1`](https://github.com/alexander-group/convert_flux/commit/b0098f1caf020ab01fc0d42e45bbc16ffca7a616))

- Data include command in pyproject.toml
  ([`e21ddc3`](https://github.com/alexander-group/convert_flux/commit/e21ddc3bb19fbc7201d6dadbed628a77a3fd6176))

### Build System

- Added FlatTransmissionCurve subclass
  ([`058a667`](https://github.com/alexander-group/convert_flux/commit/058a66760e75aac120fd6064e3f9d4698d007bdc))

- Added FlatTransmissionCurve subclass
  ([`9ed3008`](https://github.com/alexander-group/convert_flux/commit/9ed300870720a91cab7da3b1b6ef40c1cbccca6c))

- Added resampling for wavelength & transmission when they are not the same
  ([`8100002`](https://github.com/alexander-group/convert_flux/commit/81000024fa22507a464ec360b6b8360d0da8ec40))

- Change from classmethod to regular method for Vega custom equivalency
  ([`f38a8b5`](https://github.com/alexander-group/convert_flux/commit/f38a8b5c4645dbf15e8bb43729c2f541b075ab19))

- Change template spectrum file location in pyproject.toml
  ([`40b4373`](https://github.com/alexander-group/convert_flux/commit/40b4373ff6effda4cf16b0aa16074d5655748e15))

- Implementing Vega magnitude
  ([`3e814b9`](https://github.com/alexander-group/convert_flux/commit/3e814b983d50267277cf6edc897755476e4fb2c6))

- Implementing Vega magnitude
  ([`3e251b3`](https://github.com/alexander-group/convert_flux/commit/3e251b388fcfeb050a0c94f520a7208293ab959b))

- Implementing Vega magnitude
  ([`238dfe2`](https://github.com/alexander-group/convert_flux/commit/238dfe241a64c59878b63da0d122b71da3fa8922))

- Improve VegaSpec class and custom equivalency for Vega magnitude
  ([`f11d8cc`](https://github.com/alexander-group/convert_flux/commit/f11d8cc3f18aa42f91d2ae38581543c5f8f017af))

- Improve VegaSpec class and custom equivalency for Vega magnitude
  ([`87e6c45`](https://github.com/alexander-group/convert_flux/commit/87e6c459c297171076106aa074e5ff8514bfcc45))

- Initial brainstorming idea for TransmissionCurve
  ([`74c81a8`](https://github.com/alexander-group/convert_flux/commit/74c81a85aea9d30e143ba64317f2272ed1176b2e))

- Initial TransmissionCurve class and unit tests. Moved wavelength & transmission is same size check
  from FluxFluxDensity into TransmissionCurve.
  ([`b968c21`](https://github.com/alexander-group/convert_flux/commit/b968c21a3fb5663107a7e1f9a29ac074c4f99309))

- Magic mock infer_filter_info query
  ([`3a348cc`](https://github.com/alexander-group/convert_flux/commit/3a348cccf53755f6975804a88debec895e155630))

- Map VEGAMAG physical unit in the custom equivalency
  ([`03337f8`](https://github.com/alexander-group/convert_flux/commit/03337f8fe78e8584365106e1a15c48ef91d62c1e))

- Move template Vega spectrum to convert_flux directory
  ([`0ccdfaa`](https://github.com/alexander-group/convert_flux/commit/0ccdfaab1dd493df9492b48d4062993a425a0785))

- Update docstrings for Mag class
  ([`bb28d87`](https://github.com/alexander-group/convert_flux/commit/bb28d87051d347905cbabb8ed274735717b78aaf))

- Update docstrings for Mag class
  ([`3a51ec4`](https://github.com/alexander-group/convert_flux/commit/3a51ec45826d45bbae1b09d259b89b05ec06a703))

- Update docstrings for VegaSpec & Mag class
  ([`c2d91f8`](https://github.com/alexander-group/convert_flux/commit/c2d91f87431636c67fda12c7c54e35501d155f6f))

- Update docstrings for VegaSpec class
  ([`585a43e`](https://github.com/alexander-group/convert_flux/commit/585a43e3ed7add6bc6302c6a5225f0abc4a9fa74))

- Update methods for VegaSpec class
  ([`dc3dd6b`](https://github.com/alexander-group/convert_flux/commit/dc3dd6b4a677a75c904191f2a936c8a5bf6abab8))

- Update methods for VegaSpec class
  ([`ea6d362`](https://github.com/alexander-group/convert_flux/commit/ea6d362627021b418eab8cea6f35f949b3480743))

- Update methods for VegaSpec class
  ([`59242d9`](https://github.com/alexander-group/convert_flux/commit/59242d9b4066fba07543d4e77ec1e769791a177f))

- Update methods for VegaSpec class
  ([`bfed53d`](https://github.com/alexander-group/convert_flux/commit/bfed53deb7a2f04ff98eed2590c9743463712f97))

- Updates to custom equivalency for Vega magnitudes
  ([`81cb096`](https://github.com/alexander-group/convert_flux/commit/81cb0969388712b70c5938b0df2063b9cf10ed13))

### Documentation

- Log AI contributions
  ([`d6561e2`](https://github.com/alexander-group/convert_flux/commit/d6561e22091400303df5a9538c71b20100fb0da5))


## v0.2.0 (2026-11-16)

### Build System

- Define convert_flux() arguments and returns with function stub and docstring
  ([`f6fc9d5`](https://github.com/alexander-group/convert_flux/commit/f6fc9d5e831f8e25dd585d9674890705f4787a6a))

### Features

- Add AI usage logging and CLAUDE workflow preferences
  ([`3a0d94f`](https://github.com/alexander-group/convert_flux/commit/3a0d94f8f44a4d775b8a71ce97e90f269cfce765))

### Refactoring

- Reorganize imports and enhance docstrings for clarity
  ([`a0afeba`](https://github.com/alexander-group/convert_flux/commit/a0afeba640af12ae3c5f762c58c063d89a2e4f10))


## v0.1.0 (2026-10-30)

### Build System

- Add vscode directory to gitignore
  ([`caf0bc4`](https://github.com/alexander-group/convert_flux/commit/caf0bc4b7c24380f5032622a9fbd7664a33e69c1))

- Created new transmission.py to start brainstorming
  ([`c454524`](https://github.com/alexander-group/convert_flux/commit/c454524c4c18bbb6a5687f0672233fc2593f8913))

### Features

- Refactor codebase to separate helper functions and units from the source class convert_flux
  ([`efe6553`](https://github.com/alexander-group/convert_flux/commit/efe6553d9fed643b93e1a5e30312f83e43040c32))


## v0.0.3 (2026-10-26)

### Bug Fixes

- Semantic versioning not recognizing version string without prepended v
  ([`f6f0577`](https://github.com/alexander-group/convert_flux/commit/f6f0577b44cdff7e2a01596c0134a8c9481ab91f))


## v0.0.2 (2026-10-26)

### Bug Fixes

- Unit test for mag to flux density conversion updated to compare correct units in assertion
  ([`7966342`](https://github.com/alexander-group/convert_flux/commit/7966342a433196ced8e7a2acdca4a2833c83a469))


## v0.0.1 (2026-10-20)

- Initial Release
