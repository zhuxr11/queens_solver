import logging
from typing import Literal

import numpy as np
from playwright._impl._page import Page


def validate_queens_game(
    solution: np.array,
    page: Page,
    mode: Literal["linkedin"] = "linkedin",
) -> bool:
    """Validate a Queens puzzle solution using the specified backend.

    Initializes logging and dispatches to a backend-specific validator.
    Currently supports the LinkedIn Queens backend only.

    Args:
        solution: Binary solution matrix. Nonzero entries indicate queen
            positions.
        page: Page instance of the Queens game page to validate against.
        mode: Validation backend. Defaults to ``"linkedin"``.

    Returns:
        ``True`` if the solution is accepted by the game backend,
        ``False`` otherwise.

    Raises:
        RuntimeError: If validation fails during browser interaction.
        ValueError: If an unsupported ``mode`` is provided.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )
    logger = logging.getLogger("queens_validator")
    if mode == "linkedin":
        res = validate_queens_game_linkedin(
            solution=solution,
            page=page,
            logger=logger,
        )
    return res


def validate_queens_game_linkedin(
    solution: np.ndarray,
    page: Page,
    logger: logging.Logger,
) -> bool:
    """Validate a Queens puzzle solution on LinkedIn.

    Applies the solution by double-clicking enabled board cells to
    place queens, then checks for the success/confetti screen.

    Args:
        solution: Binary solution matrix. Nonzero entries indicate
            queen positions.
        page: Page instance of the LinkedIn Queens game page.
        logger: Logger for progress and debug messages.

    Returns:
        ``True`` if the game accepts the solution and displays the
        confetti animation, ``False`` otherwise.

    Raises:
        playwright.sync_api.TimeoutError: If page elements fail to
            appear within the timeout period.
        playwright.sync_api.Error: If browser interaction fails
            during automated gameplay.
    """
    # Put queens on solved tiles by double clicks
    for cell_idx in range(solution.size):
        if solution.ravel()[cell_idx] != 0:
            selector = f'div.queens-cell-with-border[data-cell-idx="{cell_idx}"]'
            page.wait_for_selector(selector)
            cell = page.query_selector(selector)

            row_idx = cell_idx // solution.shape[1] + 1
            col_idx = cell_idx % solution.shape[1] + 1
            # Place queens only on enabled tiles
            if cell.get_attribute("aria-disabled") == "false":
                cell.dblclick()
                logger.info(f"Setting [queen] on row {row_idx}, column {col_idx}")
            else:
                logger.warning(
                    f"Skip setting [queen] on row {row_idx}"
                    f", column {col_idx}, since the tile is not enabled"
                )

    # Test whether success screen shows up by detecting the confetti
    res = page.wait_for_selector("img.pr-confetti", timeout=30_000)

    logger.info(f"Validation result: {'SUCCESS' if bool(res) else 'FAILURE'}")
    return bool(res)
