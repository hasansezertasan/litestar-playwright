"""Tests for the Playwright integration."""
# ruff: noqa: C901, RUF029

from __future__ import annotations

from typing import TYPE_CHECKING
from unittest import mock

import pytest

from litestar_playwright.config import PlaywrightConfig
from litestar_playwright.plugin import PlaywrightPlugin

if TYPE_CHECKING:
    from unittest.mock import Mock

pytestmark = pytest.mark.anyio


async def test_playwright_plugin_dependencies() -> None:
    """Test that the plugin provides the correct dependencies."""
    config = PlaywrightConfig()
    plugin = PlaywrightPlugin(config)

    # Mock app config
    mock_app_config = mock.Mock()
    mock_app_config.dependencies = {}

    # Test that dependencies are provided
    result = plugin.on_app_init(mock_app_config)

    assert "browser" in result.dependencies


async def test_playwright_plugin_lifespan_integration() -> None:
    """Test that the plugin correctly adds lifespan to app config."""
    config = PlaywrightConfig()
    plugin = PlaywrightPlugin(config)

    # Mock app config
    mock_app_config = mock.Mock()
    mock_app_config.dependencies = {}
    mock_app_config.lifespan = []

    # Test that lifespan is added
    result = plugin.on_app_init(mock_app_config)

    assert config.lifespan in result.lifespan


async def test_playwright_plugin_full_integration() -> None:
    """Test full plugin integration with app config."""
    config = PlaywrightConfig()
    plugin = PlaywrightPlugin(config)

    # Mock app config
    mock_app_config = mock.Mock()
    mock_app_config.dependencies = {}
    mock_app_config.lifespan = []

    # Test full integration
    result = plugin.on_app_init(mock_app_config)

    # Verify dependencies
    assert "browser" in result.dependencies

    # Verify lifespan
    assert config.lifespan in result.lifespan

    # Verify the dependency provider is correct
    dependency = result.dependencies["browser"]
    # Type ignore because we know it's a Provide instance in this context
    assert dependency.dependency == config.provide_playwright_browser_instance  # type: ignore[union-attr]  # pylint: disable=comparison-with-callable
    assert dependency.sync_to_thread is False  # type: ignore[union-attr]


@pytest.mark.anyio
async def test_multiple_plugins_dependencies() -> None:
    """Test that multiple plugins provide different dependencies.

    Args:
        chrome_config: The Chrome configuration.
        firefox_config: The Firefox configuration.
    """
    chrome_config = PlaywrightConfig(
        playwright_instance_state_key="chrome_playwright",
        playwright_browser_instance_state_key="chrome_browser",
    )

    firefox_config = PlaywrightConfig(
        playwright_instance_state_key="firefox_playwright",
        playwright_browser_instance_state_key="firefox_browser",
    )

    chrome_plugin = PlaywrightPlugin(chrome_config)
    firefox_plugin = PlaywrightPlugin(firefox_config)

    # Mock app config
    mock_app_config = mock.Mock()
    mock_app_config.dependencies = {}
    mock_app_config.lifespan = []

    # Test Chrome plugin dependencies
    chrome_result = chrome_plugin.on_app_init(mock_app_config)
    assert "chrome_browser" in chrome_result.dependencies
    assert "chrome_playwright" in chrome_result.dependencies

    # Test Firefox plugin dependencies
    firefox_result = firefox_plugin.on_app_init(mock_app_config)
    assert "firefox_browser" in firefox_result.dependencies
    assert "firefox_playwright" in firefox_result.dependencies


@pytest.mark.anyio
async def test_multiple_plugins_lifespan() -> None:
    """Test that multiple plugins add their lifespans correctly.

    Args:
        chrome_config: The Chrome configuration.
        firefox_config: The Firefox configuration.
    """
    chrome_config = PlaywrightConfig(
        playwright_instance_state_key="chrome_playwright",
        playwright_browser_instance_state_key="chrome_browser",
    )

    firefox_config = PlaywrightConfig(
        playwright_instance_state_key="firefox_playwright",
        playwright_browser_instance_state_key="firefox_browser",
    )

    chrome_plugin = PlaywrightPlugin(chrome_config)
    firefox_plugin = PlaywrightPlugin(firefox_config)

    # Mock app config
    mock_app_config = mock.Mock()
    mock_app_config.dependencies = {}
    mock_app_config.lifespan = []

    # Test that both lifespans are added
    result = chrome_plugin.on_app_init(mock_app_config)
    result = firefox_plugin.on_app_init(result)

    assert chrome_config.lifespan in result.lifespan
    assert firefox_config.lifespan in result.lifespan


@pytest.mark.anyio
async def test_multiple_plugins_providers() -> None:
    """Test that different providers work with custom state keys.

    Args:
        chrome_config: The Chrome configuration.
        firefox_config: The Firefox configuration.
    """
    chrome_config = PlaywrightConfig(
        playwright_instance_state_key="chrome_playwright",
        playwright_browser_instance_state_key="chrome_browser",
    )

    firefox_config = PlaywrightConfig(
        playwright_instance_state_key="firefox_playwright",
        playwright_browser_instance_state_key="firefox_browser",
    )

    # Mock state with different browsers
    mock_state = mock.Mock()
    mock_chrome_browser = mock.Mock()
    mock_firefox_browser = mock.Mock()
    mock_chrome_playwright = mock.Mock()
    mock_firefox_playwright = mock.Mock()

    def mock_state_get(key: str) -> Mock | None:
        if key == "chrome_browser":
            return mock_chrome_browser
        if key == "firefox_browser":
            return mock_firefox_browser
        if key == "chrome_playwright":
            return mock_chrome_playwright
        if key == "firefox_playwright":
            return mock_firefox_playwright
        return None

    mock_state.get.side_effect = mock_state_get

    # Test Chrome providers
    chrome_browser = chrome_config.provide_playwright_browser_instance(mock_state)
    chrome_playwright = chrome_config.provide_playwright_instance(mock_state)
    assert chrome_browser == mock_chrome_browser
    assert chrome_playwright == mock_chrome_playwright

    # Test Firefox providers
    firefox_browser = firefox_config.provide_playwright_browser_instance(mock_state)
    firefox_playwright = firefox_config.provide_playwright_instance(mock_state)
    assert firefox_browser == mock_firefox_browser
    assert firefox_playwright == mock_firefox_playwright


@pytest.mark.anyio
async def test_multiple_plugins_different_browser_types() -> None:
    """Test that different browser types can be configured.

    Args:
        configs: The configurations.
    """
    configs = [
        PlaywrightConfig(
            browser_type="chromium",
            headless=True,
            playwright_instance_state_key="chromium_playwright",
            playwright_browser_instance_state_key="chromium_browser",
        ),
        PlaywrightConfig(
            browser_type="firefox",
            headless=False,
            playwright_instance_state_key="firefox_playwright",
            playwright_browser_instance_state_key="firefox_browser",
        ),
        PlaywrightConfig(
            browser_type="webkit",
            headless=True,
            playwright_instance_state_key="webkit_playwright",
            playwright_browser_instance_state_key="webkit_browser",
        ),
    ]

    for config in configs:
        plugin = PlaywrightPlugin(config)
        mock_app_config = mock.Mock()
        mock_app_config.dependencies = {}
        mock_app_config.lifespan = []

        result = plugin.on_app_init(mock_app_config)
        assert config.lifespan in result.lifespan
