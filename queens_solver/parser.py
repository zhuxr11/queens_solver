import logging
import re
from typing import Literal

from bs4 import BeautifulSoup
from playwright._impl._page import Page
from scipy.sparse import coo_matrix, csr_array


def parse_queens_game(
    page: Page,
    mode: Literal["linkedin"] = "linkedin",
) -> csr_array:
    """Parse a Queens game board using the specified backend.

    Initializes logging and dispatches to a backend-specific parser.
    Currently supports the LinkedIn Queens backend only.

    Args:
        page: Page instance of the Queens game page to parse.
        mode: Parsing backend. Defaults to ``"linkedin"``.

    Returns:
        CSR sparse matrix of the parsed board layout. Each entry holds
        the integer region/color ID for the corresponding board cell.

    Raises:
        RuntimeError: If the parser fails to locate or extract the board.
        ValueError: If an unsupported ``mode`` is provided.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )
    logger = logging.getLogger("queens_parser")
    if mode == "linkedin":
        res = parse_queens_game_linkedin(page=page, logger=logger)
    return res


def parse_queens_game_linkedin(
    page: Page,
    logger: logging.Logger | None = None,
) -> csr_array:
    """Parse a LinkedIn Queens game board into a sparse matrix.

    Extracts the rendered game board layout from the page HTML by
    locating the ``queens-board`` section and parsing each cell's
    row, column, and color class (``cell-color-X``).

    Args:
        page: Page instance of the LinkedIn Queens game page.
        logger: Logger for progress and debug messages.

    Returns:
        CSR sparse matrix of the board layout. Shape is inferred from
        parsed row/column indices; each entry holds the integer
        region/color ID from ``cell-color-X``.

    Raises:
        RuntimeError: If the ``queens-board`` section is not found in
            the HTML (e.g. user not logged in or page structure changed).
    """
    if logger is None:
        logger = logging.getLogger("queens_parser")

    html = page.content()
    soup = BeautifulSoup(html, "html.parser")

    section = soup.find("section", class_="queens-board queens-board--a11y-enabled")

    if section:
        logger.info("[queens-board] section found")
        cells = soup.find_all("div", class_="queens-cell-with-border")
        cell_indices = ([], [])
        cell_values = []
        for cell in cells:
            # ---- parse cell-color-X ----
            classes = cell.get("class", [])
            cell_color = None
            for cls in classes:
                m = re.match(r"cell-color-(\d+)", cls)
                if m:
                    cell_color = int(m.group(1))
                    cell_values.append(cell_color)
                    # ---- parse row/column ----
                    aria = cell.get("aria-label", "")
                    m = re.search(r"row\s+(\d+),\s+column\s+(\d+)", aria)
                    row = int(m.group(1))
                    col = int(m.group(2))
                    cell_indices[0].append(row - 1)
                    cell_indices[1].append(col - 1)
                    break
        mat = coo_matrix((cell_values, cell_indices))
        logger.info("Queens game board parsed")
        return mat.tocsr()
    else:
        raise RuntimeError("[queens-board] not found on the page")
