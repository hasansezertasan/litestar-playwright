"""Configuration for Playwright integration."""

from __future__ import annotations

from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Literal, cast

from playwright.async_api import Browser, BrowserType, Playwright, async_playwright

if TYPE_CHECKING:
    from typing import AsyncGenerator

    from litestar import Litestar
    from litestar.datastructures import State


@dataclass
class PlaywrightConfig:
    """Configuration for Playwright integration."""

    headless: bool = False
    """Whether to run browsers in headless mode."""

    browser_type: Literal["chromium", "firefox", "webkit"] = "chromium"
    """Type of browser to use (chromium, firefox, webkit)."""

    launch_kwargs: dict[str, Any] = field(default_factory=dict)
    """Options to pass to the "playwright.async_api.BrowserType.launch()" method.

    See https://playwright.dev/python/docs/api/class-browsertype#browser-type-launch
    for available options.
    """

    playwright_instance_state_key: str = "playwright"
    """Key used to store the playwright instance in app state."""

    playwright_browser_instance_state_key: str = "browser"
    """Key used to store the browser instance in app state."""

    @asynccontextmanager
    async def lifespan(self, app: Litestar) -> AsyncGenerator[None, None]:
        """Manage Playwright browser lifecycle.

        Args:
            app: The Litestar application instance.

        Yields:
            None: The lifespan context.
        """
        playwright = await async_playwright().start()
        browser_type: BrowserType = getattr(playwright, self.browser_type)
        launch_kwargs = {"headless": self.headless, **self.launch_kwargs}
        browser: Browser = await browser_type.launch(
            **launch_kwargs  # pyrefly: ignore[bad-argument-type]
        )

        app.state.update({
            self.playwright_instance_state_key: playwright,
            self.playwright_browser_instance_state_key: browser,
        })

        try:
            yield
        finally:
            await browser.close()
            await playwright.stop()

    def provide_playwright_browser_instance(self, state: State) -> Browser:
        """Provide the Playwright browser instance from app state.

        Args:
            state: The application state.

        Returns:
            The Playwright browser instance.
        """
        return cast("Browser", state.get(self.playwright_browser_instance_state_key))

    def provide_playwright_instance(self, state: State) -> Playwright:
        """Provide the Playwright instance from app state.

        Args:
            state: The application state.

        Returns:
            The Playwright instance.
        """
        return cast("Playwright", state.get(self.playwright_instance_state_key))
