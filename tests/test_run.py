from queens_solver.main import run


def test_run_linkedin():
    # Test linkedin backend
    run(
        url="https://linkedin.com/games/view/queens/desktop",
        mode="linkedin",
    )
