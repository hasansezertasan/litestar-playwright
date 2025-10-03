# Multiple Plugins Example

This example demonstrates how to use multiple [Litestar Playwright Plugins](https://github.com/hasansezertasan/litestar-playwright) with different configurations in a single [Litestar](https://github.com/litestar-org/litestar/) application. Each plugin provides a different browser instance that can be used for various testing scenarios.

## How to run this example

Clone the repository and navigate to this example:

```sh
git clone https://github.com/hasansezertasan/litestar-playwright.git
cd litestar-playwright/examples/multiple-plugins
```

Install the Playwright browsers:

```sh
uv run playwright install
```

Run the example using `uv`:

```sh
uv run main.py
```

## Using Docker

Remove these lines from `pyproject.toml`:

```toml
[tool.uv.sources]
litestar-playwright = { path = "../../", editable = true }
```

Update the uv lockfile:

```sh
uv lock
```

Build the Docker image:

```sh
docker build -t litestar-playwright-multiple-plugins-example -f ./Dockerfile .
docker run -p 8000:8000 litestar-playwright-multiple-plugins-example
```

## Routes

See the [Swagger UI](http://0.0.0.0:8000/schema/swagger) to see the available routes or navigate to the following routes:

- `http://0.0.0.0:8000/` - Index route
- `http://0.0.0.0:8000/all-browsers` - All browsers information
- `http://0.0.0.0:8000/chrome-info` - Chrome browser information
- `http://0.0.0.0:8000/firefox-info` - Firefox browser information
- `http://0.0.0.0:8000/webkit-info` - Webkit browser information
- `http://0.0.0.0:8000/headless-info` - Headless browser information
- `http://0.0.0.0:8000/screenshot` - Screenshot route
