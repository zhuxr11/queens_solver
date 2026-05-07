import numpy as np
from playwright.sync_api import sync_playwright
from scipy.sparse import csr_matrix

from queens_solver.parser import parse_queens_game
from queens_solver.solver import solve_queens_game
from queens_solver.utils import open_queens_game
from queens_solver.validator import validate_queens_game


def run(*args, **kwargs) -> None:
    """Run the complete Queens puzzle solving pipeline.

    This function:

    1. Parses a Queens puzzle board from the target source.
    2. Solves the puzzle using integer linear programming.
    3. Prints the formatted solution to the terminal.

    Positional and keyword arguments are forwarded directly to
    ``parse_queens_game``.

    Args:
        *args:
            Positional arguments passed to ``parse_queens_game``.

        **kwargs:
            Keyword arguments passed to ``parse_queens_game``.

    Returns:
        None
    """
    with sync_playwright() as p:
        page, mode = open_queens_game(p, *args, **kwargs)
        game_mat = parse_queens_game(page=page, mode=mode)
        game_solution = solve_queens_game(mat=game_mat)
        validation = validate_queens_game(
            solution=game_solution,
            page=page,
            mode=mode,
        )
        if not validation:
            raise RuntimeError("Validation failed")
    print_queens_solution(layout=game_mat, solution=game_solution)


def print_queens_solution(layout: csr_matrix, solution: np.ndarray) -> None:
    """Print a formatted Queens puzzle solution to the terminal.

    The board layout is displayed as a colored NumPy array where queen
    positions are highlighted using terminal color formatting.

    Internally, queen cells are represented as negative values to allow
    conditional coloring during NumPy array formatting.

    Args:
        layout:
            Sparse matrix representing the puzzle layout. Each entry
            contains the integer color ID of a cell.

        solution:
            Dense binary NumPy array indicating queen placements.

            - ``1`` indicates a queen.
            - ``0`` indicates an empty cell.

    Returns:
        None

    Notes:
        Terminal coloring is implemented using ``colorama`` and
        ``numpy.printoptions`` with a custom integer formatter.
    """
    layout_colored = (layout.toarray() + 1) * (1 - solution * 2)
    with np.printoptions(
        formatter={"int": lambda x: mark_ndarray(x)},
    ):
        print(layout_colored)


def mark_ndarray(x: int, marker: str = "*", offset: int = 0) -> str:
    """Format an integer value with optional terminal coloring.

    Negative values are highlighted using designated markers.
    Positive values are printed normally.

    The displayed value is converted to its absolute value before applying
    the optional offset.

    Args:
        x:
            Integer value to format.

        marker:
            Character as marker of queens.

        offset:
            Value added to the displayed absolute value. Defaults to ``0``.

    Returns:
        Formatted string containing optional ANSI color escape sequences.

    Example:
        ```python
        color_ndarray(-3)
        color_ndarray(5, offset=-1)
        ```
    """
    c = marker if x < 0 else " "
    return f"{abs(x) + offset}{c}"
