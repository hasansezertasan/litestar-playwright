# litestar-playwright

<!-- TODO: Make it work, make it right, make it fast. -->

[![CI](https://github.com/hasansezertasan/litestar-playwright/actions/workflows/ci.yml/badge.svg)](https://github.com/hasansezertasan/litestar-playwright/actions/workflows/ci.yml)
[![PyPI - Version](https://img.shields.io/pypi/v/litestar-playwright.svg)](https://pypi.org/project/litestar-playwright)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/litestar-playwright.svg)](https://pypi.org/project/litestar-playwright)
[![License - MIT](https://img.shields.io/github/license/hasansezertasan/litestar-playwright.svg)](https://opensource.org/licenses/MIT)
[![Latest Commit](https://img.shields.io/github/last-commit/hasansezertasan/litestar-playwright)](https://github.com/hasansezertasan/litestar-playwright)

[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![Linted and formatted with Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![GitHub Tag](https://img.shields.io/github/tag/hasansezertasan/litestar-playwright?include_prereleases=&sort=semver&color=black)](https://github.com/hasansezertasan/litestar-playwright/releases/)

[![Downloads](https://pepy.tech/badge/litestar-playwright)](https://pepy.tech/project/litestar-playwright)
[![Downloads/Month](https://pepy.tech/badge/litestar-playwright/month)](https://pepy.tech/project/litestar-playwright)
[![Downloads/Week](https://pepy.tech/badge/litestar-playwright/week)](https://pepy.tech/project/litestar-playwright)

Playwright integration for Litestar.

---

## Table of Contents

<!--toc:start-->

- [litestar-playwright](#litestar-playwright)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Simple Example](#simple-example)
  - [Multiple Playwright Plugins Example](#multiple-playwright-plugins-example)
  - [Support :envelope:](#support-envelope)
  - [Author :crown:](#author-crown)
  - [Contributing :octocat:](#contributing-octocat)
  - [Tasks](#tasks)
    - [`install`](#install)
    - [`style`](#style)
    - [`ci`](#ci)
    - [`run-simple`](#run-simple)
    - [`run-multiple-plugins`](#run-multiple-plugins)
  - [License](#license)
  - [Changelog :memo:](#changelog-memo)

<!--toc:end-->

## About

`litestar-playwright` is a plugin for [Litestar](https://litestar.dev/) that provides Playwright integration.

:sparkles: This project was born out of necessity when I was working on a project that required me to take screenshots :camera_flash:of given HTML content. I was using Playwright for this purpose, but I was not satisfied with my workflow. While improving the workflow, I started a [discussion](https://github.com/orgs/litestar-org/discussions/4249) :speech_balloon: at the Litestar Organization. Even though the discussion had zero activity :zzz:, it was a great opportunity to discover some of the internal mechanisms of Litestar. After over-engineering the workflow :nerd_face:, I decided to create a plugin for Litestar that would provide seamless Playwright integration. I learned a lot about how to use Playwright with Litestar on the way :rocket:.

## Features

- :performing_arts: **Browser Management**: Manage Playwright browser instances
- :wrench: **Dependency Injection**: Automatic injection of browser instances into route handlers
- :zap: **Async Support**: Full async/await support for all operations

## Installation

```sh
uv add litestar-playwright
```

## Usage

### Simple Example

Check out the [Quick Start](./examples/simple/README.md) example to see how to use the plugin.

### Multiple Playwright Plugins Example

Check out the [Multiple Playwright Plugins](./examples/multiple_plugins/README.md) example to see how to use multiple plugins in a single application.

## Support :envelope:

If you have any questions or need help, feel free to open an issue on the [GitHub repository][litestar-playwright].

## Contributing :octocat:

Any contributions are welcome! Please follow the [Contributing Guidelines](./CONTRIBUTING.md) to contribute to this project.

## Author :crown:

This project is maintained by [Hasan Sezer Taşan][author], It's me :wave:

## Tasks

Clone the repository and cd into the project directory:

```sh
git clone https://github.com/hasansezertasan/litestar-playwright
cd litestar-playwright
```

The commands below can also be executed using the [xc task runner](https://xcfile.dev/), which combines the usage instructions with the actual commands. Simply run `xc`, it will pop up an interactive menu with all available tasks.

### `install`

Install the dependencies:

```sh
uv sync
uv run playwright install
```

### `style`

Run the style checks:

```sh
uv run --locked tox run -e style
```

### `ci`

Run the CI pipeline:

```sh
uv run --locked tox run
```

### `run-simple`

Run the simple example:

```sh
uv run python examples/simple.py
```

### `run-multiple-plugins`

Run the multiple plugins example:

```sh
uv run python examples/multiple_plugins.py
```

## License

`litestar-playwright` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.

## Changelog :memo:

For a detailed list of changes, please refer to the [CHANGELOG](./CHANGELOG.md).

<!-- Refs -->

[author]: https://github.com/hasansezertasan
[litestar-playwright]: https://github.com/hasansezertasan/litestar-playwright
