"""Tests for the simple example application."""
# ruff: noqa: PLR2004, RUF029, TC002

from __future__ import annotations

from typing import TYPE_CHECKING

import httpx
import pytest
from examples.simple.main import app  # pyrefly: ignore[import-error]
from litestar import Litestar  # pylint: disable=wrong-import-order
from litestar.testing import AsyncTestClient  # pylint: disable=wrong-import-order

from litestar_playwright.plugin import PlaywrightPlugin

if TYPE_CHECKING:
    from typing import AsyncIterator

pytestmark = pytest.mark.anyio


@pytest.fixture(name="async_client")
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
        client: The test client for making requests.
    """
    response = await async_client.get("/")

    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Litestar Playwright Plugin is running!"


async def test_browser_info_route(async_client: AsyncTestClient[Litestar]) -> None:
    """Test the browser-info route returns browser information.

    Args:
        async_client: The test client for making requests.
    """
    response = await async_client.get("/browser-info")

    assert response.status_code == 200
    data = response.json()

    # Verify the response contains expected browser information
    assert "browser_type" in data
    assert "version" in data

    # Verify browser_type is a valid browser type
    assert data["browser_type"] in {"chromium", "firefox", "webkit"}

    # Verify version is a string and not empty
    assert isinstance(data["version"], str)
    assert len(data["version"]) > 0


async def test_browser_dependency_injection(
    async_client: AsyncTestClient[Litestar],
) -> None:
    """Test that browser dependency injection works correctly.

    Args:
        client: The test client for making requests.
    """
    # Verify that the browser dependency is registered
    dependencies = async_client.app.dependencies
    assert "browser" in dependencies

    # Get the dependency provider
    browser_provider = dependencies["browser"]

    # Verify it's configured correctly
    assert browser_provider.sync_to_thread is False


async def test_playwright_plugin_integration(
    async_client: AsyncTestClient[Litestar],
) -> None:
    """Test that the Playwright plugin is properly integrated.

    Args:
        client: The test client for making requests.
    """
    # Verify the plugin is in the app's plugins
    plugin_names = [plugin.__class__.__name__ for plugin in async_client.app.plugins]
    assert "PlaywrightPlugin" in plugin_names


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
    assert len(playwright_plugins) == 1

    plugin = playwright_plugins[0]
    assert isinstance(plugin, PlaywrightPlugin)
    assert plugin.config.headless is False
