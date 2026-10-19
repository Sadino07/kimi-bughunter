---
name: cbh-remember
description: 'Optional manual note on a target or the last confirmed finding. Capture is automatic during autopilot; this is for extra context. Usage: /remember'
type: flow
disableModelInvocation: true
whenToUse: 'Optional manual note on a target or the last confirmed finding. Capture is automatic during autopilot; this is for extra context. Usage: /remember'
---

# /remember

> **Capture is automatic.** During an engine/autopilot run, every confirmed finding is
> written to the ledger (`~/.claude/bughunter/memory/findings.jsonl`) with no action from you.
> `/remember` is only for adding an **optional manual note** — a technique detail or
> follow-up idea — that the automatic capture would not include.

## Usage

```
/remember   # then describe the note; it is appended to the target's rollup
```

## What It Is Not

This is no longer the primary way findings enter memory — the engine captures those
deterministically. Use it sparingly for human context.

---
*Adapted for Kimi Code from [Claude-BugHunter](https://github.com/elementalsouls/Claude-BugHunter) by Sachin Sharma / ElementalSoul — content CC BY 4.0.*
