import logging
from typing import Literal

from playwright._impl._browser import Browser
from playwright._impl._page import Page
from playwright._impl._playwright import Playwright


def open_queens_game(
    p: Playwright,
    mode: Literal["linkedin"] = "linkedin",
    **kwargs,
) -> tuple[Page, str]:
    """Open a Queens game page using the specified backend.

    Dispatches to a backend-specific implementation that launches and
    initializes a Queens game page. Currently supports LinkedIn only.

    Args:
        p: Active Playwright instance from ``sync_playwright()``.
        mode: Backend to use. Defaults to ``"linkedin"``.
        **kwargs: Additional keyword arguments forwarded to the
            backend-specific implementation (e.g. ``url``).

    Returns:
        Tuple of ``(page, mode)`` where ``page`` is the Playwright
        page object for the opened game.

    Raises:
        RuntimeError: If the game page cannot be opened successfully.
        ValueError: If an unsupported ``mode`` is specified.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )
    logger = logging.getLogger("queens_browser")
    if mode == "linkedin":
        res = open_queens_game_linkedin(p=p, logger=logger, **kwargs)
    return res, mode


def open_queens_game_linkedin(
    p: Playwright,
    logger: logging.Logger,
    url: str = "https://linkedin.com/games/view/queens/desktop",
) -> Page:
    """Open the LinkedIn Queens game page and start a game session.

    Launches a Chromium browser, navigates to the Queens game page,
    clicks the "Play game" button, and dismisses any tutorial modal
    with an Escape key press.

    Args:
        p: Active Playwright synchronous API instance.
        logger: Logger for progress and debug messages.
        url: URL of the LinkedIn Queens game page. Defaults to
            ``"https://linkedin.com/games/view/queens/desktop"``.

    Returns:
        Playwright ``Page`` object for the active game page after
        the game has been started.

    Raises:
        playwright.sync_api.TimeoutError: If required page elements
            fail to appear within the default timeout.
        playwright.sync_api.Error: If browser interaction fails
            during page initialization.
    """
    browser: Browser = p.chromium.launch()
    page: Page = browser.new_page()
    page.goto(url)
    page.wait_for_selector("#launch-footer-start-button")
    logger.info(f"Page loaded from: {url}")
    play_button = page.query_selector("#launch-footer-start-button")
    play_button.click()
    logger.info("[Play game] button clicked")
    # Escape possible tutorial modal dialog box
    page.keyboard.press("Escape")
    logger.info("Tutorial screen escaped")
    return page
