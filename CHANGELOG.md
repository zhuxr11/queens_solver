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
