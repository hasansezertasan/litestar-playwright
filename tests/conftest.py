"""Test configuration for the Playwright plugin."""

import pytest


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    """Set the async backend for tests.

    Returns:
        The async backend for tests.
    """
    return "asyncio"
