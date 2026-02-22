"""Configuration for Playwright integration."""
# pylint: disable=line-too-long

from __future__ import annotations

import warnings
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Literal, TypedDict, cast

from playwright.async_api import (
    Browser,
    BrowserType,
    Playwright,
    ProxySettings,
    async_playwright,
)

if TYPE_CHECKING:
    import pathlib
    from typing import AsyncGenerator

    from litestar import Litestar
    from litestar.datastructures import State


class LaunchKwargs(TypedDict, total=False):
    """Typed kwargs for ``playwright.async_api.BrowserType.launch()``."""

    executable_path: pathlib.Path | str | None
    channel: str | None
    args: list[str] | None
    ignore_default_args: bool | list[str] | None
    handle_sigint: bool | None
    handle_sigterm: bool | None
    handle_sighup: bool | None
    timeout: float | None
    env: dict[str, str]
    headless: bool | None
    devtools: bool | None
    proxy: ProxySettings | None
    downloads_path: pathlib.Path | str | None
    slow_mo: float | None
    traces_dir: pathlib.Path | str | None
    chromium_sandbox: bool | None
    firefox_user_prefs: dict[str, str | float | bool] | None


@dataclass
class PlaywrightConfig:
    """Configuration for Playwright integration."""

    browser_type: Literal["chromium", "firefox", "webkit"] = "chromium"
    """Type of browser to use (chromium, firefox, webkit)."""

    headless: bool = False
    """Whether to run browsers in headless mode."""

    launch_kwargs: LaunchKwargs = field(default_factory=LaunchKwargs)
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

        state_keys = [
            self.playwright_browser_instance_state_key,
            self.playwright_instance_state_key,
        ]
        collisions = [key for key in state_keys if key in app.state]
        if collisions:
            msg = (
                f"State key collision detected: {collisions}. "
                "Existing state will be overwritten."
            )
            warnings.warn(message=msg, stacklevel=2)

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

        Raises:
            RuntimeError: If the Playwright browser instance is not found in state.

        Returns:
            The Playwright browser instance.
        """
        browser_instance = state.get(self.playwright_browser_instance_state_key)
        if browser_instance is None:
            msg = f"Playwright browser instance not found in state under key '{self.playwright_browser_instance_state_key}'."  # noqa: E501
            raise RuntimeError(msg)
        return cast("Browser", browser_instance)

    def provide_playwright_instance(self, state: State) -> Playwright:
        """Provide the Playwright instance from app state.

        Args:
            state: The application state.

        Raises:
            RuntimeError: If the Playwright instance is not found in state.

        Returns:
            The Playwright instance.
        """
        playwright_instance = state.get(self.playwright_instance_state_key)
        if playwright_instance is None:
            msg = f"Playwright instance not found in state under key '{self.playwright_instance_state_key}'."  # noqa: E501
            raise RuntimeError(msg)
        return cast("Playwright", playwright_instance)
