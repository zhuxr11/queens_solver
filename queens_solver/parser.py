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

    This function initializes logging and dispatches board parsing
    to a backend-specific parser implementation.

    Currently, only the LinkedIn Queens backend is supported.

    Args:
        page: Page instance of the Queens game page to parse.
        mode: Parsing backend to use.

    Returns:
        A CSR sparse matrix representing the parsed Queens board layout.

        Each matrix entry contains the integer region/color ID
        associated with the corresponding board cell.

    Raises:
        RuntimeError: If the selected parser fails to locate
            or extract the Queens board.
        ValueError: If an unsupported parsing mode is provided.

    Example:
        ```python
        mat = parse_queens_game()

        print(mat.shape)
        print(mat.toarray())
        ```
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

    This function launches a Chromium browser using Playwright,
    opens the LinkedIn Queens game page, clicks the
    "Play game" button, and extracts the rendered game board
    layout from the HTML.

    Each board cell is parsed into:
        - row index
        - column index
        - region/color index

    The resulting board is returned as a SciPy CSR sparse matrix,
    where each matrix entry contains the integer region/color ID
    for the corresponding board cell.

    Args:
        page: Page instance of the LinkedIn Queens game page.
        logger: Logger instance used for progress and debug messages.

    Returns:
        A CSR sparse matrix representing the Queens board layout.

        The matrix shape is inferred from the parsed row and column
        indices. Each nonzero entry contains the parsed
        ``cell-color-X`` integer value corresponding to a board
        region/color identifier.

    Raises:
        RuntimeError: If the Queens board section cannot be found
            in the rendered HTML. This may occur if:
                - the user is not logged into LinkedIn,
                - the page structure has changed,
                - the game failed to load correctly.

    Example:
        ```python
        mat = parse_queens_game_linkedin()

        print(mat.shape)
        print(mat.toarray())
        ```
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
