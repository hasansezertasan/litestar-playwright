# litestar-playwright

<!-- TODO: Make it work, make it right, make it fast. -->

[![CI](https://github.com/hasansezertasan/litestar_playwright/actions/workflows/ci.yml/badge.svg)](https://github.com/hasansezertasan/litestar_playwright/actions/workflows/ci.yml)
[![PyPI - Version](https://img.shields.io/pypi/v/litestar_playwright.svg)](https://pypi.org/project/litestar_playwright)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/litestar_playwright.svg)](https://pypi.org/project/litestar_playwright)
[![License - MIT](https://img.shields.io/github/license/hasansezertasan/litestar_playwright.svg)](https://opensource.org/licenses/MIT)
[![Latest Commit](https://img.shields.io/github/last-commit/hasansezertasan/litestar_playwright)](https://github.com/hasansezertasan/litestar_playwright)

[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![linting - Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![GitHub Tag](https://img.shields.io/github/tag/hasansezertasan/litestar_playwright?include_prereleases=&sort=semver&color=black)](https://github.com/hasansezertasan/litestar_playwright/releases/)

[![Downloads](https://pepy.tech/badge/litestar_playwright)](https://pepy.tech/project/litestar_playwright)
[![Downloads/Month](https://pepy.tech/badge/litestar_playwright/month)](https://pepy.tech/project/litestar_playwright)
[![Downloads/Week](https://pepy.tech/badge/litestar_playwright/week)](https://pepy.tech/project/litestar_playwright)

Playwright integration for Litestar.

---

## Table of Contents

<!--toc:start-->

- [litestar-playwright](#litestar-playwright)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Installation](#installation)
  - [Quick Start](#quick-start)
  - [Configuration](#configuration)
  - [Usage](#usage)
    - [Accessing Browser Instances](#accessing-browser-instances)
    - [Web Scraping Example](#web-scraping-example)
    - [Multiple Playwright Plugins Example](#multiple-playwright-plugins-example)
  - [Support :heart:](#support-heart)
  - [Author :person_with_crown:](#author-personwithcrown)
  - [Contributing :heart:](#contributing-heart)
  - [Tasks](#tasks)
    - [`install`](#install)
    - [`style`](#style)
    - [`ci`](#ci)
    - [`run-simple`](#run-simple)
    - [`run-multiple-plugins`](#run-multiple-plugins)
  - [License](#license)
  - [Changelog :memo:](#changelog-memo)

<!--toc:end-->

## Features

- 🎭 **Browser Management**: Manage Playwright browser instances
- 🔧 **Dependency Injection**: Automatic injection of browser instances into route handlers
- ⚡ **Async Support**: Full async/await support for all operations

## Installation

```sh
uv add litestar-playwright
```

## Quick Start

```python
from litestar import Litestar
from litestar_playwright.config import PlaywrightConfig
from litestar_playwright.plugin import PlaywrightPlugin

# Create the plugin with configuration
playwright_plugin = PlaywrightPlugin(
    config=PlaywrightConfig(
        browser_type="chromium",  # or "firefox", "webkit"
        headless=False,  # Show browser windows
    )
)

# Add to your Litestar app
app = Litestar(plugins=[playwright_plugin])
```

## Configuration

The `PlaywrightConfig` class provides several configuration options:

```python
@dataclass
class PlaywrightConfig:
    headless: bool = True
    """Whether to run browsers in headless mode."""

    browser_type: str = "chromium"
    """Type of browser to use (chromium, firefox, webkit)."""

    playwright_app_state_key: str = "playwright_browser"
    """Key used to store the browser instance in app state."""
```

## Usage

### Accessing Browser Instances

The plugin automatically injects browser instances into your route handlers:

```python
from litestar import get
from playwright.async_api import Browser

@get("/my-route")
async def my_route(playwright_browser: Browser) -> str:
    # Create a new context
    context = await playwright_browser.new_context()

    # Create a new page
    page = await context.new_page()

    # Navigate to a URL
    await page.goto("https://example.com")

    return "Page loaded!"
```

### Web Scraping Example

Here's a complete example of web scraping with the plugin:

```python
from litestar import get
from playwright.async_api import Browser

@get("/scrape")
async def scrape_website(playwright_browser: Browser) -> dict:
    # Create a new context
    context = await playwright_browser.new_context()

    try:
        # Create a new page
        page = await context.new_page()

        # Navigate to a website
        await page.goto("https://example.com")

        # Extract information
        title = await page.title()
        content = await page.content()

        return {
            "title": title,
            "content_length": len(content)
        }
    finally:
        # Always clean up
        await context.close()
```

### Multiple Playwright Plugins Example

You can use multiple Playwright plugins in a single application for different use cases:

```python
from litestar import Litestar, get
from playwright.async_api import Browser
from litestar_playwright.config import PlaywrightConfig
from litestar_playwright.plugin import PlaywrightPlugin

# Create different configurations for various browsers
chrome_config = PlaywrightConfig(
    browser_type="chromium",
    headless=False,
    launch_kwargs={"args": ["--no-sandbox"]},
    playwright_browser_instance_state_key="chrome_browser",
)

firefox_config = PlaywrightConfig(
    browser_type="firefox",
    headless=False,
    playwright_browser_instance_state_key="firefox_browser",
)

# Route handlers can inject specific browser instances
@get("/chrome-info")
async def chrome_info(chrome_browser: Browser) -> dict:
    return {"browser": chrome_browser.browser_type.name}

@get("/firefox-info")
async def firefox_info(firefox_browser: Browser) -> dict:
    return {"browser": firefox_browser.browser_type.name}

# Use multiple plugins in your app
app = Litestar(
    plugins=[
        PlaywrightPlugin(config=chrome_config),
        PlaywrightPlugin(config=firefox_config),
    ],
    route_handlers=[chrome_info, firefox_info],
)
```

This approach is useful for:

- **Cross-browser testing**: Test your application across different browsers
- **Specialized workflows**: Use different browsers for different tasks
- **CI/CD scenarios**: Run headless browsers for automated testing
- **Performance testing**: Compare behavior across browser engines

## Support :heart:

If you have any questions or need help, feel free to open an issue on the [GitHub repository][litestar_playwright].

## Author :person_with_crown:

This project is maintained by [Hasan Sezer Taşan][author], It's me :wave:

## Contributing :heart:

Any contributions are welcome! Please follow the [Contributing Guidelines](./CONTRIBUTING.md) to contribute to this project.

## Tasks

Clone the repository and cd into the project directory:

```sh
git clone https://github.com/hasansezertasan/litestar_playwright
cd litestar_playwright
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
[litestar_playwright]: https://github.com/hasansezertasan/litestar-playwright
