# Queens Solver

Queens Solver solves "Queens" game hosted on [linkedin](https://linkedin.com/games/queens) with linear programming.

## Installation

To install `queens_solver`, first run one of the following:

``` {bash}
# Using pip
pip install queens_solver

# Using uv
uv pip install queens_solver
```

Then, run this to install browsers for playwright:

``` {bash}
install-playwright-browsers
```

## Usage

`queens_solver` automatically loads the "Queens" game hosted daily. To call the solver, run:

``` {bash}
queens-solver
```

The solver first loads the game, then solves it, and finally validates the solution on the hosted webpage. Positions of queens are marked by asterisks to the right of color index. An example output looks like:

```
2026-05-08 12:45:44,409 [INFO] queens_parser: [queens-board] section found
2026-05-08 12:45:44,413 [INFO] queens_parser: Queens game board parsed
2026-05-08 12:45:44,414 [INFO] queens_solver: Added equality constraint: one queen per row
2026-05-08 12:45:44,414 [INFO] queens_solver: Added equality constraint: one queen per column
2026-05-08 12:45:44,414 [INFO] queens_solver: Added equality constraint: one queen per color
2026-05-08 12:45:44,415 [INFO] queens_solver: Combined equality constraints
2026-05-08 12:45:44,415 [INFO] queens_solver: Added upper-bound constraint: at most one queen per diagonally-adjacent tiles (\)
2026-05-08 12:45:44,416 [INFO] queens_solver: Added upper-bound constraint: at most one queen per diagonally-adjacent tiles (/)
2026-05-08 12:45:44,417 [INFO] queens_solver: Combined upper-bound constraints
2026-05-08 12:45:44,417 [INFO] queens_solver: Generated target coefficients for score function
2026-05-08 12:45:44,427 [INFO] queens_solver: Solved linear programming
2026-05-08 12:45:44,596 [WARNING] queens_validator: Skip setting [queen] on row 1, column 5, since the tile is not enabled
2026-05-08 12:45:44,617 [WARNING] queens_validator: Skip setting [queen] on row 2, column 7, since the tile is not enabled
2026-05-08 12:45:44,729 [INFO] queens_validator: Setting [queen] on row 3, column 2
2026-05-08 12:45:44,821 [INFO] queens_validator: Setting [queen] on row 4, column 4
2026-05-08 12:45:45,444 [INFO] queens_validator: Setting [queen] on row 5, column 1
2026-05-08 12:45:45,509 [INFO] queens_validator: Setting [queen] on row 6, column 3
2026-05-08 12:45:45,591 [INFO] queens_validator: Setting [queen] on row 7, column 6
2026-05-08 12:45:49,158 [INFO] queens_validator: Validation result: SUCCESS
[[1  1  1  1  2* 2  2 ]
 [1  1  3  3  3  2  4*]
 [1  3* 3  3  3  3  4 ]
 [1  3  5  5* 5  3  4 ]
 [1* 3  3  3  3  3  6 ]
 [1  3  7* 7  7  3  6 ]
 [7  7  7  7  6  6* 6 ]]
```
