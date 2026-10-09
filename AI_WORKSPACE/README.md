# Online ↔ Local AI Workspace Bridge

## Purpose

This folder is the handoff layer between two complementary environments:

- **Online reasoning workspace:** explore ideas, synthesize concepts, design architecture, research, and author durable specifications.
- **Local execution workspace:** inspect the actual checkout, edit code, run commands and tests, observe failures, and return concrete evidence.

The goal is one continuous work process without pretending the two environments share a live filesystem or automatic memory.

## Canonical sources of truth

1. **The repository and its current Git history** establish what has actually been committed.
2. **The local working tree** establishes what currently exists on the user's computer, including uncommitted work.
3. `PROJECT_STATE.md` records the last jointly verified project snapshot. It may be stale; verify it against the repository and local machine.
4. `NEXT_TASK.md` defines the current intended operation. It is a plan, not proof that the operation occurred.
5. `HANDOFF_TEMPLATE.md` structures the evidence returned from each work session.

Never claim a local file was changed, a command was run, or a test passed merely because a specification was written in an online conversation.

## Work loop

1. **Orient:** inspect the current repository, active branch, local Git status, relevant docs, and actual code.
2. **Specify:** write the intended change, constraints, and acceptance checks into a durable task.
3. **Execute:** the local agent implements the task on a working branch and runs relevant checks.
4. **Report:** record changed paths, test commands and results, errors, and remaining uncertainty.
5. **Review:** compare the result with the original intent; inspect diffs instead of trusting summaries alone.
6. **Update:** revise project state and create the next task only after the new state is verified.

## Branch and safety policy

- Do not overwrite or reset a user's uncommitted work.
- Before switching branches, inspect `git status --short --branch`.
- Use a feature branch for substantive work; review the diff before merging.
- Keep a task small enough to inspect and test.
- Preserve existing names, notation, conceptual scope, and architecture unless the task explicitly calls for changing them.
- Do not reorganize, mass-format, delete, or rewrite the large knowledge corpus as part of an unrelated task.
- Separate facts verified from repository evidence, local-machine evidence, assumptions, and proposals.
- If online and local work conflict, stop and reconcile the actual diffs. Do not silently choose one side.

## Files

- `PROJECT_STATE.md` — repository facts, current unknowns, and baseline.
- `NEXT_TASK.md` — immediate local operation and acceptance criteria.
- `LOCAL_AGENT_INSTRUCTIONS.md` — operating contract for an agent on the user's computer.
- `HANDOFF_TEMPLATE.md` — standard record for returning execution evidence.

## Important boundary

GitHub is the shared transport and durable record, not a live connection to the user's computer. Online commits become local only after a fetch and checkout/merge; local changes become visible online only after commit and push. Keep this boundary explicit in every handoff.
