"""Tests for the litestar_playwright.config module."""
# ruff: noqa: DOC501, RUF029, TRY301

from unittest import mock

import pytest

from litestar_playwright.config import PlaywrightConfig

pytestmark = pytest.mark.anyio


async def test_playwright_config_defaults() -> None:
    """Test Playwright configuration defaults."""
    config = PlaywrightConfig()

    assert config.headless is False
    assert config.browser_type == "chromium"
    assert config.playwright_browser_instance_state_key == "browser"


async def test_playwright_config_custom_values() -> None:
    """Test Playwright configuration with custom values."""
    config = PlaywrightConfig(
        headless=False,
        browser_type="firefox",
        playwright_instance_state_key="custom_playwright",
        playwright_browser_instance_state_key="custom_browser",
    )

    assert config.headless is False
    assert config.browser_type == "firefox"
    assert config.playwright_instance_state_key == "custom_playwright"
    assert config.playwright_browser_instance_state_key == "custom_browser"


async def test_playwright_config_provider() -> None:
    """Test that the config provider function works correctly."""
    config = PlaywrightConfig()

    # Mock state
    mock_state = mock.Mock()
    mock_browser = mock.Mock()

    mock_state.get.return_value = mock_browser

    # Test browser provider
    browser = config.provide_playwright_browser_instance(mock_state)
    assert browser == mock_browser

    # Verify the correct key was used
    mock_state.get.assert_called_once_with("browser")


async def test_playwright_config_provider_custom_key() -> None:
    """Test that the config provider function works with custom state key."""
    config = PlaywrightConfig(playwright_browser_instance_state_key="custom_browser")

    # Mock state
    mock_state = mock.Mock()
    mock_browser = mock.Mock()

    mock_state.get.return_value = mock_browser

    # Test browser provider
    browser = config.provide_playwright_browser_instance(mock_state)
    assert browser == mock_browser

    # Verify the correct key was used
    mock_state.get.assert_called_once_with("custom_browser")


async def test_playwright_lifespan_success() -> None:
    """Test successful lifespan management."""
    config = PlaywrightConfig(browser_type="chromium", headless=True)

    # Mock app
    mock_app = mock.Mock()
    mock_app.state = {}

    # Mock playwright
    mock_browser = mock.AsyncMock()
    mock_playwright_instance = mock.AsyncMock()
    mock_playwright_instance.chromium.launch.return_value = mock_browser
    mock_playwright = mock.AsyncMock()
    mock_playwright.start.return_value = mock_playwright_instance

    with mock.patch(
        "litestar_playwright.config.async_playwright", return_value=mock_playwright
    ):
        async with config.lifespan(mock_app):
            # Verify browser was launched
            mock_playwright_instance.chromium.launch.assert_called_once_with(
                headless=True
            )

            # Verify state was updated
            assert mock_app.state["browser"] == mock_browser
            assert mock_app.state["playwright"] == mock_playwright_instance

        # Verify cleanup
        mock_browser.close.assert_called_once()
        mock_playwright_instance.stop.assert_called_once()


async def test_playwright_lifespan_firefox() -> None:
    """Test lifespan management with Firefox browser."""
    config = PlaywrightConfig(browser_type="firefox", headless=False)

    # Mock app
    mock_app = mock.Mock()
    mock_app.state = {}

    # Mock playwright
    mock_browser = mock.AsyncMock()
    mock_playwright_instance = mock.AsyncMock()
    mock_playwright_instance.firefox.launch.return_value = mock_browser
    mock_playwright = mock.AsyncMock()
    mock_playwright.start.return_value = mock_playwright_instance

    with mock.patch(
        "litestar_playwright.config.async_playwright", return_value=mock_playwright
    ):
        async with config.lifespan(mock_app):
            # Verify Firefox browser was launched
            mock_playwright_instance.firefox.launch.assert_called_once_with(
                headless=False
            )

            # Verify state was updated
            assert mock_app.state["browser"] == mock_browser
            assert mock_app.state["playwright"] == mock_playwright_instance


async def test_playwright_lifespan_webkit() -> None:
    """Test lifespan management with WebKit browser."""
    config = PlaywrightConfig(browser_type="webkit", headless=True)

    # Mock app
    mock_app = mock.Mock()
    mock_app.state = {}

    # Mock playwright
    mock_browser = mock.AsyncMock()
    mock_playwright_instance = mock.AsyncMock()
    mock_playwright_instance.webkit.launch.return_value = mock_browser
    mock_playwright = mock.AsyncMock()
    mock_playwright.start.return_value = mock_playwright_instance

    with mock.patch(
        "litestar_playwright.config.async_playwright", return_value=mock_playwright
    ):
        async with config.lifespan(mock_app):
            # Verify WebKit browser was launched
            mock_playwright_instance.webkit.launch.assert_called_once_with(
                headless=True
            )

            # Verify state was updated
            assert mock_app.state["browser"] == mock_browser
            assert mock_app.state["playwright"] == mock_playwright_instance


async def test_playwright_lifespan_cleanup_on_exception() -> None:
    """Test that cleanup happens even when an exception occurs."""
    config = PlaywrightConfig()

    # Mock app
    mock_app = mock.Mock()
    mock_app.state = {}

    # Mock playwright
    mock_browser = mock.AsyncMock()
    mock_playwright_instance = mock.AsyncMock()
    mock_playwright_instance.chromium.launch.return_value = mock_browser
    mock_playwright = mock.AsyncMock()
    mock_playwright.start.return_value = mock_playwright_instance

    with mock.patch(
        "litestar_playwright.config.async_playwright", return_value=mock_playwright
    ):
        try:
            async with config.lifespan(mock_app):
                msg = "Test exception"
                raise RuntimeError(msg)
        except RuntimeError:
            pass

        # Verify cleanup still happened
        mock_browser.close.assert_called_once()
        mock_playwright_instance.stop.assert_called_once()


@pytest.mark.anyio
async def test_multiple_plugins_configuration() -> None:
    """Test that multiple plugins can be configured with different settings.

    Args:
        chrome_config: The Chrome configuration.
        firefox_config: The Firefox configuration.
    """
    chrome_config = PlaywrightConfig(
        browser_type="chromium",
        headless=True,
        playwright_instance_state_key="chrome_playwright",
        playwright_browser_instance_state_key="chrome_browser",
    )

    firefox_config = PlaywrightConfig(
        browser_type="firefox",
        headless=False,
        playwright_instance_state_key="firefox_playwright",
        playwright_browser_instance_state_key="firefox_browser",
    )

    # Verify configurations are different
    assert chrome_config.browser_type == "chromium"
    assert firefox_config.browser_type == "firefox"
    assert chrome_config.headless is True
    assert firefox_config.headless is False
    assert chrome_config.playwright_browser_instance_state_key == "chrome_browser"
    assert firefox_config.playwright_browser_instance_state_key == "firefox_browser"


@pytest.mark.anyio
async def test_multiple_plugins_custom_launch_kwargs() -> None:
    """Test that different browser options can be configured.

    Args:
        chrome_config: The Chrome configuration.
        firefox_config: The Firefox configuration.
    """
    chrome_config = PlaywrightConfig(
        browser_type="chromium",
        launch_kwargs={"args": ["--no-sandbox", "--disable-dev-shm-usage"]},
        playwright_instance_state_key="chrome_playwright",
        playwright_browser_instance_state_key="chrome_browser",
    )

    firefox_config = PlaywrightConfig(
        browser_type="firefox",
        launch_kwargs={"firefox_user_prefs": {"dom.webnotifications.enabled": False}},
        playwright_instance_state_key="firefox_playwright",
        playwright_browser_instance_state_key="firefox_browser",
    )

    # Verify different browser options
    assert chrome_config.launch_kwargs["args"] == [
        "--no-sandbox",
        "--disable-dev-shm-usage",
    ]
    assert firefox_config.launch_kwargs["firefox_user_prefs"] == {
        "dom.webnotifications.enabled": False
    }
