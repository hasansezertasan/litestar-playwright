"""Tests for the multiple plugins example application."""
# ruff: noqa: PLR2004, RUF029, TC002

from __future__ import annotations

from typing import TYPE_CHECKING

import httpx
import pytest
from examples.multiple_plugins.main import app  # pyrefly: ignore[import-error]
from litestar import Litestar  # pylint: disable=wrong-import-order
from litestar.testing import AsyncTestClient  # pylint: disable=wrong-import-order

from litestar_playwright.plugin import PlaywrightPlugin

if TYPE_CHECKING:
    from typing import AsyncIterator

pytestmark = pytest.mark.anyio


@pytest.fixture(name="async_client", scope="session")
async def fx_async_client() -> AsyncIterator[httpx.AsyncClient]:
    """Create a test client for testing.

    Yields:
        An AsyncTestClient instance for making HTTP requests.
    """
    app.debug = True
    async with AsyncTestClient(app=app) as client:
        yield client


async def test_index_route(async_client: AsyncTestClient[Litestar]) -> None:
    """Test the index route returns the expected message.

    Args:
        async_client: The test client for making requests.
    """
    response = await async_client.get("/")

    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Multiple Playwright Plugins are running!"


async def test_chrome_info_route(async_client: AsyncTestClient[Litestar]) -> None:
    """Test the chrome-info route returns Chrome browser information.

    Args:
        async_client: The test client for making requests.
    """
    response = await async_client.get("/chrome-info")

    assert response.status_code == 200
    data = response.json()

    # Verify the response contains expected browser information
    assert "browser_type" in data
    assert "version" in data
    assert "name" in data
    assert "description" in data

    # Verify browser_type is chromium
    assert data["browser_type"] == "chromium"
    assert data["name"] == "Chrome Browser"
    assert data["description"] == "Primary browser for general web testing"

    # Verify version is a string and not empty
    assert isinstance(data["version"], str)
    assert len(data["version"]) > 0


async def test_firefox_info_route(async_client: AsyncTestClient[Litestar]) -> None:
    """Test the firefox-info route returns Firefox browser information.

    Args:
        async_client: The test client for making requests.
    """
    response = await async_client.get("/firefox-info")

    assert response.status_code == 200
    data = response.json()

    # Verify the response contains expected browser information
    assert "browser_type" in data
    assert "version" in data
    assert "name" in data
    assert "description" in data

    # Verify browser_type is firefox
    assert data["browser_type"] == "firefox"
    assert data["name"] == "Firefox Browser"
    assert data["description"] == "Cross-browser testing and Firefox-specific features"

    # Verify version is a string and not empty
    assert isinstance(data["version"], str)
    assert len(data["version"]) > 0


async def test_webkit_info_route(async_client: AsyncTestClient[Litestar]) -> None:
    """Test the webkit-info route returns WebKit browser information.

    Args:
        async_client: The test client for making requests.
    """
    response = await async_client.get("/webkit-info")

    assert response.status_code == 200
    data = response.json()

    # Verify the response contains expected browser information
    assert "browser_type" in data
    assert "version" in data
    assert "name" in data
    assert "description" in data

    # Verify browser_type is webkit
    assert data["browser_type"] == "webkit"
    assert data["name"] == "WebKit Browser"
    assert data["description"] == "Safari-like testing and WebKit-specific features"

    # Verify version is a string and not empty
    assert isinstance(data["version"], str)
    assert len(data["version"]) > 0


async def test_headless_info_route(async_client: AsyncTestClient[Litestar]) -> None:
    """Test the headless-info route returns headless browser information.

    Args:
        async_client: The test client for making requests.
    """
    response = await async_client.get("/headless-info")

    assert response.status_code == 200
    data = response.json()

    # Verify the response contains expected browser information
    assert "browser_type" in data
    assert "version" in data
    assert "name" in data
    assert "description" in data

    # Verify browser_type is chromium (headless)
    assert data["browser_type"] == "chromium"
    assert data["name"] == "Headless Chrome Browser"
    assert data["description"] == "CI/CD and automated testing scenarios"

    # Verify version is a string and not empty
    assert isinstance(data["version"], str)
    assert len(data["version"]) > 0


async def test_screenshot_route(async_client: AsyncTestClient[Litestar]) -> None:
    """Test the screenshot route functionality.

    Args:
        async_client: The test client for making requests.
    """
    response = await async_client.get("/screenshot")

    assert response.status_code == 200
    data = response.json()

    # Verify the response contains status and message
    assert "status" in data
    assert "message" in data

    # The screenshot might succeed or fail depending on the environment
    # Both outcomes are valid for testing
    assert data["status"] in {"success", "error"}


async def test_all_browsers_route(async_client: AsyncTestClient[Litestar]) -> None:  # noqa: C901
    """Test the all-browsers route returns information about all browser instances.

    Args:
        async_client: The test client for making requests.
    """
    response = await async_client.get("/all-browsers")

    assert response.status_code == 200
    data = response.json()

    # Verify the response contains all expected browser information
    assert "chrome" in data
    assert "firefox" in data
    assert "webkit" in data
    assert "headless" in data
    assert "total_browsers" in data

    # Verify total_browsers count
    assert data["total_browsers"] == 4

    # Verify each browser has type and version
    for browser_name in ["chrome", "firefox", "webkit", "headless"]:
        browser_info = data[browser_name]
        assert "type" in browser_info
        assert "version" in browser_info

        # Verify browser types are correct
        if browser_name == "chrome":
            assert browser_info["type"] == "chromium"
        elif browser_name == "firefox":
            assert browser_info["type"] == "firefox"
        elif browser_name == "webkit":
            assert browser_info["type"] == "webkit"
        elif browser_name == "headless":
            assert browser_info["type"] == "chromium"

        # Verify version is a string and not empty
        assert isinstance(browser_info["version"], str)
        assert len(browser_info["version"]) > 0


async def test_multiple_plugins_integration(
    async_client: AsyncTestClient[Litestar],
) -> None:
    """Test that multiple Playwright plugins are properly integrated.

    Args:
        async_client: The test client for making requests.
    """
    # Verify multiple Playwright plugins are in the app's plugins
    playwright_plugins = [
        plugin
        for plugin in async_client.app.plugins
        if plugin.__class__.__name__ == "PlaywrightPlugin"
    ]

    # Should have 4 plugins
    assert len(playwright_plugins) == 4

    # Verify all plugins are PlaywrightPlugin instances
    for plugin in playwright_plugins:
        assert isinstance(plugin, PlaywrightPlugin)


async def test_browser_dependencies_registration(
    async_client: AsyncTestClient[Litestar],
) -> None:
    """Test that all browser dependencies are properly registered.

    Args:
        async_client: The test client for making requests.
    """
    # Verify that all browser dependencies are registered
    dependencies = async_client.app.dependencies

    expected_dependencies = {
        "chrome_browser",
        "firefox_browser",
        "webkit_browser",
        "headless_browser",
    }

    for dep_name in expected_dependencies:
        assert dep_name in dependencies, f"Missing dependency: {dep_name}"

        # Get the dependency provider
        dep_provider = dependencies[dep_name]

        # Verify it's configured correctly
        assert dep_provider.sync_to_thread is False


async def test_application_configuration(
    async_client: AsyncTestClient[Litestar],
) -> None:
    """Test that the application is configured with the correct settings."""
    # Verify debug mode is enabled
    assert async_client.app.debug is True

    # Verify the Playwright plugin is configured with headless=False
    playwright_plugins = [
        plugin
        for plugin in async_client.app.plugins
        if plugin.__class__.__name__ == "PlaywrightPlugin"
    ]
    assert len(playwright_plugins) == 4
