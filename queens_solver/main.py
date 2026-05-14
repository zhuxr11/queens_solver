import numpy as np
from playwright.sync_api import sync_playwright
from scipy.sparse import csr_matrix

from queens_solver.browser import open_queens_game
from queens_solver.parser import parse_queens_game
from queens_solver.solver import solve_queens_game
from queens_solver.validator import validate_queens_game


def run(*args, **kwargs) -> None:
    """Run the complete Queens puzzle solving pipeline.

    Parses the board, solves it with integer linear programming,
    validates the solution in-browser, then prints the result.

    Args:
        \*args: Positional arguments forwarded to
            ``parse_queens_game``.
        \*\*kwargs: Keyword arguments forwarded to
            ``parse_queens_game``.
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

    Queen cells are represented as negative values for conditional
    color formatting via ``numpy.printoptions`` with a custom
    integer formatter.

    Args:
        layout: Sparse matrix of the puzzle layout. Each entry holds
            the integer color ID of a cell.
        solution: Dense binary array. ``1`` indicates a queen, ``0``
            an empty cell.
    """
    layout_colored = (layout.toarray() + 1) * (1 - solution * 2)
    with np.printoptions(
        formatter={"int": lambda x: mark_ndarray(x)},
    ):
        print(layout_colored)


def mark_ndarray(x: int, marker: str = "*", offset: int = 0) -> str:
    """Format an integer value with optional terminal coloring.

    Negative values are highlighted with ``marker``; positive values
    are printed normally. The displayed value is shown as its absolute
    value plus ``offset``.

    Args:
        x: Integer value to format.
        marker: Character used to mark queen positions. Defaults
                to ``"*"``.
        offset: Value added to the displayed absolute value. Defaults
                to ``0``.

    Returns:
        Formatted string with ANSI color escape sequences.
    """
    c = marker if x < 0 else " "
    return f"{abs(x) + offset}{c}"
