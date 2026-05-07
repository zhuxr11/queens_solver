import logging
from typing import Literal

import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix, csr_array, vstack


def solve_queens_game(mat: csr_array) -> np.ndarray:
    """Solve a LinkedIn Queens puzzle using integer linear programming.

    This function formulates the Queens puzzle as a binary integer linear
    programming problem and solves it with ``scipy.optimize.linprog``.

    The following constraints are enforced:

    - Exactly one queen per row.
    - Exactly one queen per column.
    - Exactly one queen per color region.
    - No two queens may touch diagonally.

    The objective function maximizes the number of placed queens while
    satisfying all constraints.

    Args:
        mat:
            Sparse matrix representation of the puzzle board. Each entry
            contains the integer color ID of a cell. The matrix shape
            corresponds to the puzzle dimensions.

    Returns:
        A dense binary NumPy array of shape ``(n_row, n_col)`` where:

        - ``1`` indicates a queen is placed in the cell.
        - ``0`` indicates the cell is empty.

    Raises:
        RuntimeError:
            If the linear programming solver fails to find a valid solution.

    Notes:
        The optimization problem is solved as a binary integer linear
        program with:

        - Equality constraints for rows, columns, and color regions.
        - Upper-bound constraints for diagonal adjacency.
        - Binary decision variables representing queen placement.

    Example:
        ```python
        board = parse_queens_game()
        solution = solve_queens_game(board)

        print(solution)
        ```
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )
    logger = logging.getLogger("queens_solver")
    # One queen per row
    eq_mat_row = gen_constraint_mat(mat, mode="row")
    logger.info("Added equality constraint: one queen per row")
    # One queen per column
    eq_mat_col = gen_constraint_mat(mat, mode="column")
    logger.info("Added equality constraint: one queen per column")
    # One queen per color
    eq_mat_color = gen_constraint_mat(mat, mode="color")
    logger.info("Added equality constraint: one queen per color")
    # Combine equation constraint matrix
    eq_mat = vstack([eq_mat_row, eq_mat_col, eq_mat_color])
    eq_vec = np.array([1] * eq_mat.shape[0])
    logger.info("Combined equality constraints")

    # Queens should not touch diagonally
    le_mat_lu = gen_constraint_mat(mat, mode="\\")
    logger.info(
        "Added upper-bound constraint: at most one queen"
        " per diagonally-adjacent tiles (\\)"
    )
    le_mat_ru = gen_constraint_mat(mat, mode="/")
    logger.info(
        "Added upper-bound constraint: at most one queen"
        " per diagonally-adjacent tiles (/)"
    )
    # Combine less-equation constraint matrix
    le_mat = vstack([le_mat_lu, le_mat_ru])
    le_vec = np.array([1] * le_mat.shape[0])
    logger.info("Combined upper-bound constraints")

    # Target matrix
    target_vec = np.array([-1] * mat.size)
    logger.info("Generated target coefficients for score function")

    # Solve linear programming
    res = linprog(
        c=target_vec,
        A_ub=le_mat,
        b_ub=le_vec,
        A_eq=eq_mat,
        b_eq=eq_vec,
        bounds=(0, 1),
        integrality=True,
    )
    logger.info("Solved linear programming")
    if not res.success:
        raise RuntimeError(
            f"Linear programming failed with status: {res.status}"
            f" after {res.nit} iteration(s)"
        )
    return res.x.reshape(mat.shape).astype(np.int64)


def gen_constraint_mat(
    mat: csr_array,
    mode: Literal["row", "column", "color", "/", "\\"],
) -> csr_array:
    """Generate a sparse constraint coefficient matrix for the Queens puzzle.

    This function constructs sparse matrices used in the integer linear
    programming formulation of the Queens puzzle. Different constraint
    types can be generated depending on the specified ``mode``.

    Supported constraint modes include:

    - ``"row"``:
      Generates constraints enforcing one queen per row.

    - ``"column"``:
      Generates constraints enforcing one queen per column.

    - ``"color"``:
      Generates constraints enforcing one queen per color region.

    - ``"\\"``:
      Generates constraints preventing queens from touching along
      descending diagonals.

    - ``"/"``:
      Generates constraints preventing queens from touching along
      ascending diagonals.

    Args:
        mat:
            Sparse matrix representation of the puzzle board. Each entry
            contains the integer color ID of a cell.

        mode:
            Constraint type to generate. Must be one of:

            - ``"row"``
            - ``"column"``
            - ``"color"``
            - ``"\\"``
            - ``"/"``

    Returns:
        A CSR sparse matrix representing the linear constraint coefficients
        for the specified constraint type.

        - For ``"row"``, ``"column"``, and ``"color"``, rows correspond
          to equality constraints.
        - For ``"\\"`` and ``"/"``, rows correspond to upper-bound
          constraints for diagonally adjacent cells.

    Notes:
        Each column in the returned matrix corresponds to a flattened board
        cell in row-major order:

        ```python
        linear_idx = row * n_col + col
        ```

        The generated matrices are intended for use with
        ``scipy.optimize.linprog``.

    Example:
        ```python
        row_constraints = gen_constraint_mat(board, "row")
        color_constraints = gen_constraint_mat(board, "color")
        diag_constraints = gen_constraint_mat(board, "\\")
        ```
    """
    _, n_col = mat.shape
    mat_indices = ([], [])
    if mode in ["row", "column"]:
        # Coefficient matrix that sums up queens by rows/columns
        if mode == "row":

            def op(a: int, b: int) -> int:
                return a // b
        else:

            def op(a: int, b: int) -> int:
                return a % b

        for idx in range(mat.size):
            mat_indices[0].append(op(idx, n_col))
            mat_indices[1].append(idx)
        res = coo_matrix(([1] * mat.size, mat_indices)).tocsr()
    elif mode == "color":
        # Coefficient matrix that sums up queens by colors
        mat_coo = mat.tocoo()
        for idx in range(mat_coo.nnz):
            mat_indices[0].append(mat_coo.data[idx])
            linear_idx = mat_coo.row[idx] * n_col + mat_coo.col[idx]
            mat_indices[1].append(linear_idx)
        res = coo_matrix(([1] * mat_coo.nnz, mat_indices)).tocsr()
    elif mode in ["\\", "/"]:
        # Coefficient matrix that sums up queens by diagonally adjacent tiles
        if mode == "\\":
            idx_offset = n_col + 1
        else:
            idx_offset = n_col - 1
        cur_row = 0
        for idx in range(mat.size):
            if mode == "\\":
                idx_mask = (idx + 1) % n_col
            else:
                idx_mask = idx % n_col
            if idx_mask != 0 and idx + idx_offset < mat.size:
                mat_indices[0].append(cur_row)
                mat_indices[1].append(idx)
                mat_indices[0].append(cur_row)
                mat_indices[1].append(idx + idx_offset)
                cur_row += 1
        res = coo_matrix(
            ([1] * cur_row * 2, mat_indices),
            shape=(cur_row, mat.size),
        ).tocsr()
    return res
