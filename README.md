# Static Code Analysis for the Boutros Lab

[![GitHub release](https://img.shields.io/github/v/release/uclahs-cds/tool-static-analysis)](https://github.com/uclahs-cds/tool-static-analysis/actions/workflows/prepare-release.yaml)

Run static analyses for code style, linting, and repository configuration.

## Usage
```yaml
---
name: CI

on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main

jobs:
  static-analysis:
    runs-on: ubuntu-latest

    steps:
      - uses: uclahs-cds/tool-static-analysis@v1
        # The below is optional and shows the default value
        with:
          docker-tag: latest
```

## Versioning

Per [GitHub's advice](https://docs.github.com/en/actions/creating-actions/about-custom-actions#using-tags-for-release-management) for release management, this repository uses semantic version tags. The key details are:

* Full semantic version tags, such as `v1.0.2`, are immutable and will always refer to the same commit hash.
* Major version tags, such as `v1` or `v2`, are kept up-to-date with the latest matching semantic version tag.

Callers should use the latest major version tag (currently `v1`), as that will refer to the most recent stable and backwards-compatible version. Specifying semantic version tags is discouraged unless there is a specific need for absolute reproducibility.


## License

Author: Nicholas Wiltsie (nwiltsie@mednet.ucla.edu)

tool-static-analysis is licensed under the GNU General Public License version 2. See the file LICENSE.md for the terms of the GNU GPL license.

GitHub automations common to the Boutros Lab repositories.

Copyright (C) 2024 University of California Los Angeles ("Boutros Lab") All rights reserved.

This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
