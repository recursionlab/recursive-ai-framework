# Local Agent Operating Contract

You are operating inside the user's actual checkout of `recursionlab/recursive-ai-framework`. Your advantage is direct access to local files, tools, command output, and tests. Use that access to establish facts rather than guessing from prior conversation.

## Before acting

1. Read this file and `AI_WORKSPACE/PROJECT_STATE.md`.
2. Read `AI_WORKSPACE/NEXT_TASK.md`.
3. Inspect `git status --short --branch`, the current branch, and the latest commit.
4. Inspect the relevant code and source documents before editing.
5. If the local state contradicts the workspace notes, trust observed local/repository evidence and update the notes with the discrepancy.

## Fidelity rules

- Preserve the user's actual objective, terminology, distinctions, and intended scope.
- Do not silently replace an unusual or ambitious concept with a more conventional neighboring concept.
- Do not interpret a plan as an implemented feature, an asserted result as a verified result, or a test command as a passing test.
- Distinguish observed facts, hypotheses, recommendations, and unresolved questions.
- When interpreting a user request, address the claim actually presented before evaluating it. Do not weaken it through unneeded qualifications or change the success criterion without saying so.
- Challenge an assumption when evidence warrants it, and identify the evidence. Fidelity is not automatic agreement.

## Editing rules

- Implement the smallest coherent change that meets the current task.
- Do not mass-reformat, rename, delete, or reorganize unrelated files.
- Preserve symbolic notation and naming conventions unless the task requires modification.
- Prefer narrow diffs and existing project patterns.
- Never discard local changes to make the branch convenient.
- Do not expose secrets, tokens, or local credential files in repository changes.

## Verification rules

- Run relevant checks where feasible.
- Report exact commands and whether each passed, failed, or was not run.
- Include meaningful failure output, not just "tests failed."
- Inspect the final diff for unintended changes.
- Do not claim the work is complete if acceptance criteria remain unmet.

## Closing every task

Update `AI_WORKSPACE/HANDOFF_TEMPLATE.md` (copy the template into a dated handoff file or append a dated entry) with:
- Intent and acceptance criteria.
- Files inspected and changed.
- Commands run and results.
- Decisions made and why.
- Discrepancies from the plan.
- Remaining blockers and uncertainty.
- The next smallest useful action.

Commit and push only when the user-authorized workflow calls for it. Otherwise, leave changes inspectable locally and return the diff and results. After pushing, report the branch and commit SHA so the online workspace can inspect the exact artifact.
