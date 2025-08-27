"""Simple Example. Read the README.md for more information."""
# ruff: noqa: S104, RUF029

from typing import Dict

import uvicorn
from litestar import Litestar, get
from playwright.async_api import Browser

from litestar_playwright.config import PlaywrightConfig
from litestar_playwright.plugin import PlaywrightPlugin


@get("/")
async def index() -> Dict[str, str]:
    """Show that the plugin is working with a simple index route.

    Returns:
        A dictionary containing a message indicating that the plugin is running.
    """
    return {"message": "Litestar Playwright Plugin is running!"}


@get("/browser-info")
async def browser_info(browser: Browser) -> Dict[str, str]:
    """Get information about the browser instance.

    Args:
        browser: The browser instance.

    Returns:
        A dictionary containing information about the browser instance.
    """
    return {
        "browser_type": browser.browser_type.name,
        "version": browser.version,
    }


app = Litestar(
    plugins=[PlaywrightPlugin(config=PlaywrightConfig(headless=True))],
    route_handlers=[index, browser_info],
    debug=True,
)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
