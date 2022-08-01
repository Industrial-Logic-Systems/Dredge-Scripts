# CHANGELOG

## [v1.2.7](https://github.com/Industrial-Logic-Systems/Dredge-Scripts/releases/tag/v1.2.7) - 2022-08-01 17:18:20

## What's Changed

## :wrench: Fixes & Refactoring

- fix: Add PUMP\_OUT\_ON to csv for hopper dredges @Frazzer951 (#57)

## :busts_in_silhouette: List of contributors

@Frazzer951

### Bug Fixes

- general:
  - fix errors in tests ([18bb19a](https://github.com/Industrial-Logic-Systems/Dredge-Scripts/commit/18bb19a820f753fbbb20e5d96973af777f939508)) ([#57](https://github.com/Industrial-Logic-Systems/Dredge-Scripts/pull/57))
  - Add PUMP_OUT_ON to csv for hopper dredges ([05518f9](https://github.com/Industrial-Logic-Systems/Dredge-Scripts/commit/05518f9f16af5bd38039ae28aea1a498e55ca970)) ([#57](https://github.com/Industrial-Logic-Systems/Dredge-Scripts/pull/57))
  - flip lat and long for hopper dredge ([c71f675](https://github.com/Industrial-Logic-Systems/Dredge-Scripts/commit/c71f675c8579636541674daba59ce8c24510c048))

### Refactor

- general:
  - rename test to tests ([5246154](https://github.com/Industrial-Logic-Systems/Dredge-Scripts/commit/5246154d2778a1d4ebf2de7e9244deb282f7fa84))
  - rename tests to test ([fa71394](https://github.com/Industrial-Logic-Systems/Dredge-Scripts/commit/fa7139468b7e97c23bb3ab4f83d7f395c3e5f817))

### Continuous Integration

- general:
  - auto changelog ([ac026d5](https://github.com/Industrial-Logic-Systems/Dredge-Scripts/commit/ac026d55875d5572e046691b382c500bf427f91c))

### Chore

- general:
  - remove unneeded package versions ([094ef47](https://github.com/Industrial-Logic-Systems/Dredge-Scripts/commit/094ef47eda2ff8239355af8a40617542a6a7aada)) ([#57](https://github.com/Industrial-Logic-Systems/Dredge-Scripts/pull/57))

## [v1.2.6](https://github.com/Industrial-Logic-Systems/Dredge-Scripts/releases/tag/v1.2.6) - 2022-07-15 19:38:13

**Full Changelog**: https://github.com/Industrial-Logic-Systems/Dredge-Scripts/compare/v1.2.5...v1.2.6

### Bug Fixes

- general:
  - fix tests ([7b45790](https://github.com/Industrial-Logic-Systems/Dredge-Scripts/commit/7b45790ecbcb04381ff39f9c1f61157ed8ab5bae))
  - Various Bug Fixed with hopper Dredges ([d64d020](https://github.com/Industrial-Logic-Systems/Dredge-Scripts/commit/d64d020e36e1f58354548c4740caaaaa1f945181))
  - Pin pyModbusTCP version ([97c84b5](https://github.com/Industrial-Logic-Systems/Dredge-Scripts/commit/97c84b55d79e3f7009c25c4a0c75ca7b581cacc6))

### Refactor

- general:
  - change how string is formatted ([6a0eab4](https://github.com/Industrial-Logic-Systems/Dredge-Scripts/commit/6a0eab4cc7ff94b12062e3e43c377fbf7acef158))

### Continuous Integration

- general:
  - update dependabot config ([8faeac4](https://github.com/Industrial-Logic-Systems/Dredge-Scripts/commit/8faeac410c380600b707713e3e67925beb5bfd34))

### Chore

- general:
  - edit configs ([0e1f2e0](https://github.com/Industrial-Logic-Systems/Dredge-Scripts/commit/0e1f2e043fb5002c3b2bc4077b21d886b63f32e8))
  - pin packages ([8d3e763](https://github.com/Industrial-Logic-Systems/Dredge-Scripts/commit/8d3e763e58d8f7e5a4b643ee1856c11f11c56b27))

## [v1.2.5](https://github.com/Industrial-Logic-Systems/Dredge-Scripts/releases/tag/v1.2.5) - 2022-06-09 19:25:06

## What's Changed

## :wrench: Fixes & Refactoring

- better error handling @Frazzer951 (#47)
- remove old dweet code that wasnt used @Frazzer951 (#46)

## :arrow_up: Dependencies updates

- :arrow\_up: Bump release-drafter/release-drafter from 5.19.0 to 5.20.0 @dependabot (#44)
- :arrow\_up: Bump actions/setup-python from 3 to 4 @dependabot (#45)

## :busts_in_silhouette: List of contributors

@Frazzer951, @dependabot and @dependabot[bot]

## [v1.2.4](https://github.com/Industrial-Logic-Systems/Dredge-Scripts/releases/tag/v1.2.4) - 2022-04-27 17:39:28

## What's Changed

## :rocket: Features

- Add Product Key To GUI @Frazzer951 (#43)
- Product Key @Frazzer951 (#40)

## :arrow_up: Dependencies updates

- :arrow\_up: Bump github/codeql-action from 1 to 2 @dependabot (#42)
- :arrow\_up: Bump codecov/codecov-action from 2 to 3 @dependabot (#39)

## :hammer: Maintenance

- Add More Tests @Frazzer951 (#41)

## :white_check_mark: Tests

- Add More Tests @Frazzer951 (#41)

## :busts_in_silhouette: List of contributors

@Frazzer951, @dependabot and @dependabot[bot]

## [v1.2.3](https://github.com/Industrial-Logic-Systems/Dredge-Scripts/releases/tag/v1.2.3) - 2022-03-28 19:10:49

## What's Changed

## :rocket: Features

- Feature: Add current version to GUI @Frazzer951 (#31)

## :package: Build System & CI/CD

- add of test for json @Frazzer951 (#33)

## :arrow_up: Dependencies updates

- :arrow\_up: Bump release-drafter/release-drafter from 5.18.1 to 5.19.0 @dependabot (#38)
- :arrow\_up: Bump actions/checkout from 2 to 3 @dependabot (#37)
- :arrow\_up: Bump actions/setup-python from 2 to 3 @dependabot (#36)

## :hammer: Maintenance

- Add tests @Frazzer951 (#34)
- TOX Now creates coverage.xml for CodeCov @Frazzer951 (#32)

## :white_check_mark: Tests

- Add tests @Frazzer951 (#34)
- add of test for json @Frazzer951 (#33)

## :busts_in_silhouette: List of contributors

@Frazzer951, @dependabot and @dependabot[bot]

### Bug Fixes

- general:
  - fix directory name for auto labeler ([61c5f78](https://github.com/Industrial-Logic-Systems/Dredge-Scripts/commit/61c5f78bd5ea669ff014a8f2ca8559bdb0a51d5f)) ([#34](https://github.com/Industrial-Logic-Systems/Dredge-Scripts/pull/34))

## [v1.2.2](https://github.com/Industrial-Logic-Systems/Dredge-Scripts/releases/tag/v1.2.2) - 2022-02-15 18:49:13

## What's Changed

## :wrench: Fixes & Refactoring

- Fix: Header not updating when modbus variables get updated @Frazzer951 (#30)

## :arrow_up: Dependencies updates

- :arrow\_up: Bump release-drafter/release-drafter from 5.17.6 to 5.18.1 @dependabot (#29)

## :busts_in_silhouette: List of contributors

@Frazzer951, @dependabot and @dependabot[bot]

## [v1.2.1](https://github.com/Industrial-Logic-Systems/Dredge-Scripts/releases/tag/v1.2.1) - 2022-01-21 19:11:09

## What's Changed

## :rocket: Features

- Init function @Frazzer951 (#27)
- Failed Dweets will now save to a file @Frazzer951 (#25)

## :hammer: Maintenance

- Update Logging @Frazzer951 (#26)
- Add XML Tests @Frazzer951 (#24)

## :white_check_mark: Tests

- Add XML Tests @Frazzer951 (#24)

## :busts_in_silhouette: List of contributors

@Frazzer951 and Luke Eltiste

## [v1.2.0](https://github.com/Industrial-Logic-Systems/Dredge-Scripts/releases/tag/v1.2.0) - 2022-01-20 19:44:29

## What's Changed

## :rocket: Features

- Basic Startup Screen @Frazzer951 (#17)
- Image Generation Now Modular @Frazzer951 (#14)

## :wrench: Fixes & Refactoring

- fix some bug to get it running smoothly  @Frazzer951 (#23)
- Basic Startup Screen @Frazzer951 (#17)
- Image Generation Now Modular @Frazzer951 (#14)
- log loop can handle multiple dredge types @Frazzer951 (#10)
- refactor config.py @Frazzer951 (#8)
- Convert to module @Frazzer951 (#5)

## :arrow_up: Dependencies updates

- :arrow\_up: Bump release-drafter/release-drafter from 5.17.5 to 5.17.6 @dependabot (#19)
- :arrow\_up: Bump pre-commit from 2.16.0 to 2.17.0 @dependabot (#18)
- :arrow\_up: Bump numpy from 1.22.0 to 1.22.1 @dependabot (#13)
- :arrow\_up: Bump release-drafter/release-drafter from 5.16.1 to 5.17.5 @dependabot (#7)
- cleanup project config files and setup package versioning @Frazzer951 (#12)
- :arrow\_up: Bump release-drafter/release-drafter from 5.15.0 to 5.16.1 @dependabot (#6)

## :hammer: Maintenance

- [ImgBot] Optimize images @imgbot (#22)
- File cleanup @Frazzer951 (#21)
- Update tox and Build @Frazzer951 (#20)
- various cleanups and setup pre-commit @Frazzer951 (#15)
- cleanup project config files and setup package versioning @Frazzer951 (#12)
- update logging @Frazzer951 (#11)
- update release-drafter @Frazzer951 (#9)

## :white_check_mark: Tests

- update test folder to match updates @Frazzer951 (#16)

## :busts_in_silhouette: List of contributors

@Frazzer951, @ImgBotApp, @dependabot, @dependabot[bot], @imgbot and Luke Eltiste

### Bug Fixes

- general:
  - fix typo ([72bea58](https://github.com/Industrial-Logic-Systems/Dredge-Scripts/commit/72bea58df9448864d522a259f2d9e4bc5d0c64a0))
  - fix more workflows ([f42af61](https://github.com/Industrial-Logic-Systems/Dredge-Scripts/commit/f42af61c7fbc78b302ee05a5d5a17c7fc4832372)) ([#5](https://github.com/Industrial-Logic-Systems/Dredge-Scripts/pull/5))

### Refactor

- general:
  - refactor config.py ([b85c253](https://github.com/Industrial-Logic-Systems/Dredge-Scripts/commit/b85c2532597870514a1d76f87d4951ef23f07843)) ([#8](https://github.com/Industrial-Logic-Systems/Dredge-Scripts/pull/8))
  - refactoring: format codebase with black ([2fdb713](https://github.com/Industrial-Logic-Systems/Dredge-Scripts/commit/2fdb713d7643e7f22e6849ff792db226d4f9126b)) ([#5](https://github.com/Industrial-Logic-Systems/Dredge-Scripts/pull/5))

### Chore

- general:
  - chore - remove rainbow ([0466fcb](https://github.com/Industrial-Logic-Systems/Dredge-Scripts/commit/0466fcb6e333c99e7f6a77b20d34fabb1e6dbc9d))
  - update release-drafter ([3fc9afb](https://github.com/Industrial-Logic-Systems/Dredge-Scripts/commit/3fc9afb7f15ba78b592da4bd93d54764e1fb1eb7))

## [1.1.1](https://github.com/Industrial-Logic-Systems/Dredge-Scripts/releases/tag/1.1.1) - 2021-12-13 18:51:55

*No description*

### Bug Fixes

- general:
  - fix file save error ([6ed5cd7](https://github.com/Industrial-Logic-Systems/Dredge-Scripts/commit/6ed5cd7008d91a9ce0938850107d68006e9c4337))
  - fix workflow ([a30b2b3](https://github.com/Industrial-Logic-Systems/Dredge-Scripts/commit/a30b2b3c69c2ea40c73206cc3437e71d15e8e021))
  - fix some errors ([b09eeab](https://github.com/Industrial-Logic-Systems/Dredge-Scripts/commit/b09eeab2ca8e8aef8a5f72cceb94caf40c120d3f))
  - fix some errors ([93fe2d8](https://github.com/Industrial-Logic-Systems/Dredge-Scripts/commit/93fe2d83a369275bfd8b0ed80886bed28d6a42ca))

\* *This CHANGELOG was automatically generated by [auto-generate-changelog](https://github.com/BobAnkh/auto-generate-changelog)*
