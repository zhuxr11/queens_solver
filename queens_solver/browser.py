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

    This function dispatches to a backend-specific implementation
    that launches and initializes a Queens game page in a browser.

    Currently, only the LinkedIn Queens backend is supported.

    Args:
        p: Active Playwright instance created by
            `sync_playwright()`.
        mode: Backend implementation used to open the game.
        **kwargs: Additional keyword arguments passed to the
            backend-specific implementation.

            Common arguments include:
                url: URL of the Queens game page for the backend.

    Returns:
        A tuple containing:

            - Playwright page object for the opened game page.
            - Backend mode used to open the game.

    Raises:
        RuntimeError: If the game page cannot be opened or
            initialized successfully.
        ValueError: If an unsupported backend mode is specified.

    Example:
        ```python
        with sync_playwright() as p:
            page, mode = open_queens_game(
                p=p,
                logger=logger,
                url="https://www.linkedin.com/games/view/queens/desktop",
            )
        ```
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

    This function launches a Chromium browser using Playwright,
    opens the LinkedIn Queens game page, waits for the
    "Play game" button to appear, and clicks it to enter
    the playable game board.

    After launching the game, the function sends an Escape
    key press to dismiss a possible tutorial modal dialog
    that may otherwise block interactions with the board.

    Args:
        p: Active Playwright synchronous API instance.
        logger: Logger instance used for progress and debug
            messages.
        url: URL of the LinkedIn Queens game page.

    Returns:
        A Playwright ``Page`` object representing the active
        Queens game page after the game has been started.

    Raises:
        playwright.sync_api.TimeoutError: If required page
            elements fail to appear within the default timeout.
        playwright.sync_api.Error: If browser interaction
            fails during page initialization.

    Example:
        ```python
        with sync_playwright() as p:
            page = open_queens_game_linkedin(
                p=p,
                url="https://www.linkedin.com/games/view/queens/desktop",
                logger=logger,
            )

            html = page.content()
        ```
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
