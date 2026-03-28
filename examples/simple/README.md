# Simple Example

This example demonstrates how to use the [Litestar Playwright Plugin](https://github.com/hasansezertasan/litestar-playwright) with [Litestar](https://github.com/litestar-org/litestar/) application.

## How to run this example

Clone the repository and navigate to this example:

```sh
git clone https://github.com/hasansezertasan/litestar-playwright.git
cd litestar-playwright/examples/simple
```

Install the Playwright browsers:

```sh
uv run playwright install
```

Run the example using `uv`:

```sh
uv run main.py
```

Or run it with Docker:

```sh
docker build -f examples/simple/Dockerfile -t litestar-playwright-simple .
docker run --rm -p 8000:8000 litestar-playwright-simple
```


See the [Swagger UI](http://0.0.0.0:8000/schema/swagger) to see the available routes or navigate to the following routes:

- `http://0.0.0.0:8000/` - Index route
- `http://0.0.0.0:8000/browser-info` - Browser information
