## v0.1.13 (2026-05-11)

### Refactor

- **.github.workflows.upload-pypi**: Shorten the label for the workflow.

## v0.1.12 (2026-05-11)

### Fix

- **.github.workflows.github-actions-ci-cd**: Add "outputs" sections to "check_author" and "check_tag".

### Refactor

- **.github.workflows.github-actions-ci-cd**: Revise labels for "check_author" and "check_tag".

## v0.1.11 (2026-05-11)

### Fix

- **.github.workflows.github-actions-ci-cd**: Remove criteria on "check_tag".

## v0.1.10 (2026-05-11)

### Fix

- **.github.workflows.github-actions-ci-cd**: Add print of detected author and tag.

## v0.1.9 (2026-05-11)

### Fix

- **pyproject**: Add package name to "tool.hatch.build.targets.wheel", since the project name (queens-slvr) differs from the package name (queens_solver).
- **.github.workflows.github-actions-ci-cd**: Fix missing arguments and typos in CI/CD workflow file.
- **.github.workflows.github-actions-ci-cd**: Add "build package" to "build" step.
- **pyproject**: Change package name (queens-slvr, as published on PyPI), and update "README.md" accordingly.

### Refactor

- **.github.workflows.github-actions-ci-cd**: Extrack check of commit author and tag, and use them to determine whether to skip "publish" or "release".

## v0.1.8 (2026-05-09)

### Fix

- **.github.workflows.github-actions-ci-cd**: Use "github.event.repository.name" instead of "github.repository.name".

## v0.1.7 (2026-05-09)

### Fix

- **.github.workflows.github-actions-ci-cd**: Update "actions/create-release" (v1 to v1.1.4).
- **.github.workflows.github-actions-ci-cd**: Use repo name instead of whole repo (user/name) in "release".

## v0.1.6 (2026-05-09)

### Fix

- **.github.workflows.github-actions-ci-cd**: Check the latest tag is on the latest commit and starts with "v" in "release" step.

## v0.1.5 (2026-05-09)

### Fix

- **.github.workflows.github-actions-ci-cd**: Add proceed criteria to all following steps in "publish" and "release".

## v0.1.4 (2026-05-09)

### Fix

- **.github.workflows.github-actions-ci-cd**: Change "github.actor" (action triggerer) to commit author as criteria to trigger "publish" (authored not by bot) and "release" (authored by bot).

## v0.1.3 (2026-05-09)

### Fix

- **.github.workflows.github-actions-ci-cd**: Put "release" after "tests" instead of "publish".
- **queens_solver.browser**: Remove `logger` from `open_queens_game()`.
- **.github.workflows.github-actions-ci-cd**: Trigger "publish" only on master and commits not authored by action bot; trigger "release" only on manual runs and a tag starting with "v" by action bot.

### Refactor

- **queens_solver.browser**: Remove `url` from `open_queens_game()` arguments and update its docstring accordingly.

## v0.1.2 (2026-05-08)

### Fix

- **.github.workflows.github-actions-ci-cd**: Remove criteria about bot-triggered commits and "run_release" variable from "workflow_dispatch".

## v0.1.1 (2026-05-08)

### Fix

- **.github.workflows.github-actions-ci-cd**: Remove step "codecov" and set "release" go after "publish", triggered manually, since bot-created pushes do NOT trigger actions.
- **.github.workflows.github-actions-ci-cd**: Fix a bug when rebasing dev to master in "publish" step.

## v0.1.0 (2026-05-08)

### Feat

- Initialize queens solver project.

### Fix

- **.github.workflows.github-actions-ci-cd**: Resolve the "invalid refspec 'HEAD:refs/tags/*'" error.
- **.github.workflows.github-actions-ci-cd**: Add "PAT_TOKEN" to push to protected branches in "publish" step.
- **.github.workflows.github-actions-ci-cd**: Fix a mistake in replacing "Install Playwright browsers" in "tests" step.
- **.github.workflows.github-actions-ci-cd**: Add `uv run` before scripts managed by "uv".
- **.github.workflows.github-actions-ci-cd**: Add rebasing "dev" branch (if exists) after pushing the version bump commit on "master".
- **.github.workflows.github-actions-ci-cd**: Add logger output to "pytest".
- **.github.workflows.github-actions-ci-cd**: Update "actions/upload-artifact" (v4to v7) to avoid "Node.js 20 actions" warnings.
- **.github.workflows.github-actions-ci-cd**: Update "actions/checkout" (v4 to v6) and "astral-sh/setup-uv" (v6 to v8.1.0) to avoid "Node.js 20 actions" warnings.
- **.github.workflows.github-actions-ci-cd**: Add "pytest-cov" to run coverage with "pytest".
- **.github.workflows.github-actions-ci-cd**: Remove use of uv-generated scripts (e.g. install-playwright-browsers), since they result in "command not found" errors in CI/CD.
