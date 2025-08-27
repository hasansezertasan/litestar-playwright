"""Multiple Playwright Plugins Example. Read the README.md for more information."""
# ruff: noqa: E501, S104, RUF029

from typing import Any, Dict

import uvicorn
from litestar import Litestar, get
from playwright.async_api import Browser, Page

from litestar_playwright.config import PlaywrightConfig
from litestar_playwright.plugin import PlaywrightPlugin


@get("/")
async def index() -> Dict[str, str]:
    """Show that the plugin is working with a simple index route.

    Returns:
        A dictionary containing a message indicating that the multiple plugins are running.
    """
    return {"message": "Multiple Playwright Plugins are running!"}


@get("/chrome-info")
async def chrome_info(chrome_browser: Browser) -> Dict[str, Any]:
    """Get information about the Chrome browser instance.

    Args:
        chrome_browser: Chrome browser instance injected by the plugin.

    Returns:
        A dictionary containing information about the Chrome browser instance.
    """
    return {
        "browser_type": chrome_browser.browser_type.name,
        "version": chrome_browser.version,
        "name": "Chrome Browser",
        "description": "Primary browser for general web testing",
    }


@get("/firefox-info")
async def firefox_info(firefox_browser: Browser) -> Dict[str, Any]:
    """Get information about the Firefox browser instance.

    Args:
        firefox_browser: Firefox browser instance injected by the plugin.

    Returns:
        A dictionary containing information about the Firefox browser instance.
    """
    return {
        "browser_type": firefox_browser.browser_type.name,
        "version": firefox_browser.version,
        "name": "Firefox Browser",
        "description": "Cross-browser testing and Firefox-specific features",
    }


@get("/webkit-info")
async def webkit_info(webkit_browser: Browser) -> Dict[str, Any]:
    """Get information about the WebKit browser instance.

    Args:
        webkit_browser: WebKit browser instance injected by the plugin.

    Returns:
        A dictionary containing information about the WebKit browser instance.
    """
    return {
        "browser_type": webkit_browser.browser_type.name,
        "version": webkit_browser.version,
        "name": "WebKit Browser",
        "description": "Safari-like testing and WebKit-specific features",
    }


@get("/headless-info")
async def headless_info(headless_browser: Browser) -> Dict[str, Any]:
    """Get information about the headless Chrome browser instance.

    Args:
        headless_browser: Headless Chrome browser instance injected by the plugin.

    Returns:
        A dictionary containing information about the headless browser instance.
    """
    return {
        "browser_type": headless_browser.browser_type.name,
        "version": headless_browser.version,
        "name": "Headless Chrome Browser",
        "description": "CI/CD and automated testing scenarios",
    }


@get("/screenshot")
async def take_screenshot(chrome_browser: Browser) -> Dict[str, str]:
    """Take a screenshot using the Chrome browser instance.

    Args:
        chrome_browser: Chrome browser instance injected by the plugin.

    Returns:
        A dictionary containing information about the screenshot status.
    """
    try:
        page: Page = await chrome_browser.new_page()
        await page.goto("https://example.com")
        await page.screenshot(path="screenshot.png")
        await page.close()
    except Exception as e:  # noqa: BLE001, pylint: disable=broad-exception-caught
        return {"status": "error", "message": str(e)}
    return {"status": "success", "message": "Screenshot saved as screenshot.png"}


@get("/all-browsers")
async def all_browsers_info(
    chrome_browser: Browser,
    firefox_browser: Browser,
    webkit_browser: Browser,
    headless_browser: Browser,
) -> Dict[str, Any]:
    """Get information about all browser instances.

    Args:
        chrome_browser: Chrome browser instance.
        firefox_browser: Firefox browser instance.
        webkit_browser: WebKit browser instance.
        headless_browser: Headless Chrome browser instance.

    Returns:
        A dictionary containing information about all browser instances.
    """
    return {
        "chrome": {
            "type": chrome_browser.browser_type.name,
            "version": chrome_browser.version,
        },
        "firefox": {
            "type": firefox_browser.browser_type.name,
            "version": firefox_browser.version,
        },
        "webkit": {
            "type": webkit_browser.browser_type.name,
            "version": webkit_browser.version,
        },
        "headless": {
            "type": headless_browser.browser_type.name,
            "version": headless_browser.version,
        },
        "total_browsers": 4,
    }


# Create different Playwright configurations for various use cases
chrome_config = PlaywrightConfig(
    browser_type="chromium",
    headless=True,
    playwright_instance_state_key="chrome_playwright",
    playwright_browser_instance_state_key="chrome_browser",
    launch_kwargs={"args": ["--no-sandbox", "--disable-dev-shm-usage"]},
)

firefox_config = PlaywrightConfig(
    browser_type="firefox",
    headless=True,
    playwright_instance_state_key="firefox_playwright",
    playwright_browser_instance_state_key="firefox_browser",
    launch_kwargs={"firefox_user_prefs": {"dom.webnotifications.enabled": False}},
)

webkit_config = PlaywrightConfig(
    browser_type="webkit",
    headless=True,
    playwright_instance_state_key="webkit_playwright",
    playwright_browser_instance_state_key="webkit_browser",
    launch_kwargs={"args": ["--disable-web-security"]},
)

headless_config = PlaywrightConfig(
    browser_type="chromium",
    headless=True,
    playwright_instance_state_key="headless_playwright",
    playwright_browser_instance_state_key="headless_browser",
    launch_kwargs={
        "args": [
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--disable-gpu",
            "--disable-web-security",
        ]
    },
)

# Create the Litestar application with multiple Playwright plugins
app = Litestar(
    plugins=[
        PlaywrightPlugin(config=chrome_config),
        PlaywrightPlugin(config=firefox_config),
        PlaywrightPlugin(config=webkit_config),
        PlaywrightPlugin(config=headless_config),
    ],
    route_handlers=[
        index,
        chrome_info,
        firefox_info,
        webkit_info,
        headless_info,
        take_screenshot,
        all_browsers_info,
    ],
    debug=True,
)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
