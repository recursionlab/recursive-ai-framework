# Next Task — Connect the Local Checkout Safely

**Task ID:** BRIDGE-001  
**Status:** Ready for local execution  
**Objective:** Make the user's existing local checkout aware of `bridge/online-local-workflow` without losing local changes or assuming the checkout is clean.

## Step 1 — Inspect before changing anything

In PowerShell, open the directory that is already the local clone of `recursive-ai-framework` and run:

```powershell
git status --short --branch
git remote -v
git branch --show-current
git log -1 --oneline
```

Record the output. Confirm that the remote points to the expected repository.

**Stop condition:** If Git reports modified, staged, or untracked work that might matter, do not reset, clean, stash, or overwrite it. Record it and decide how to preserve it before switching branches.

## Step 2 — Fetch the bridge branch

```powershell
git fetch origin
git branch -r --list origin/bridge/online-local-workflow
```

If the branch is present and the working tree is safe to switch:

```powershell
git switch --track -c bridge/online-local-workflow origin/bridge/online-local-workflow
```

If a local branch with that name already exists, inspect it first and switch to it only after verifying its tracking and status. Do not blindly overwrite it.

## Step 3 — Verify the bridge artifacts

```powershell
git status --short --branch
git log -1 --oneline
Get-Content .\AI_WORKSPACE\README.md
Get-Content .\AI_WORKSPACE\PROJECT_STATE.md
Get-Content .\AI_WORKSPACE\NEXT_TASK.md
```

Confirm these files are present in the working checkout and the branch is the intended one.

## Step 4 — Return an evidence-based handoff

Report:
- Local repository path.
- Current branch and latest commit.
- Whether the working tree was clean before switching.
- Whether the branch switch succeeded.
- Any local changes that prevented switching.
- Active local agent/IDE, if known.
- Any errors verbatim.

Do not start a code refactor during this task. The acceptance criterion is a safe, verified bridge—not a claim that the local agent and online chat now share a live filesystem.

## Acceptance criteria

- [ ] Correct repository confirmed.
- [ ] Existing local changes preserved.
- [ ] Bridge branch fetched and checked out, or the blocker documented.
- [ ] Bridge documents verified locally.
- [ ] Actual command output recorded in the handoff.

## After this task

Choose one bounded first implementation target from the existing project. Inspect the related theory and code, define a small change with testable acceptance criteria, then execute it locally and return the diff and test results.
