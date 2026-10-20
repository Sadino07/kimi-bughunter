# kimi-bughunter

**Claude-BugHunter, converted and kept up-to-date for [Kimi Code CLI](https://www.kimi.com/code/docs/en/).**

This repo tracks [`elementalsouls/Claude-BugHunter`](https://github.com/elementalsouls/Claude-BugHunter)
(83 bug-hunting skills + 15 engagement commands) and re-publishes it in the
Kimi Code skill format. A daily GitHub Action re-converts the upstream repo
whenever it changes, validates every skill, and pushes the update — so this
mirror never goes stale.

All methodology credit goes to **Sachin Sharma / ElementalSoul**. Skill content
is **CC BY 4.0** (attribution preserved at the foot of every `SKILL.md`); the
conversion tooling here is MIT. See [NOTICE](NOTICE).

## Install

```bash
git clone https://github.com/Sadino07/kimi-bughunter.git
cp -r kimi-bughunter/skills/* ~/.kimi-code/skills/
```

Restart your Kimi Code session. Skills auto-load by topic — describe what you
are testing in plain language and the right skill loads.

The 15 upstream slash commands become manually-invoked flow skills:

```
/skill:cbh-hunt target.com     # active vulnerability hunting
/skill:cbh-recon target.com    # full recon pipeline
/skill:cbh-triage              # 7-Question Gate on a finding
/skill:cbh-report              # submission-ready report
/skill:cbh-autopilot target    # autonomous hunt loop
... (cbh-scope, cbh-validate, cbh-surface, cbh-chain, cbh-intel,
     cbh-pickup, cbh-remember, cbh-memory-gc, cbh-token-scan, cbh-web3-audit)
```

## What is adapted for Kimi

| Upstream (Claude) | Here (Kimi Code) |
| --- | --- |
| `description`-only frontmatter | `description` + `whenToUse` + `type` |
| slash commands (`/hunt`) | `cbh-*` flow skills (`/skill:cbh-hunt`) |
| `$TARGET`, `$1` in bodies | `$target` (`arguments: target`), Kimi-safe placeholders |
| manual updates | daily `sync-upstream` workflow + validator |

## Sync bot

`.github/workflows/sync-upstream.yml` runs daily (and on demand):

1. clones the upstream repo,
2. runs `convert_to_kimi.py --clean`,
3. runs `validate_skills.py` (frontmatter schema, name/dir match, no dupes),
4. commits and pushes **only if validation passes and the output changed**,
5. opens an issue if anything fails.

## Local use (without this repo)

```bash
python3 convert_to_kimi.py                      # → ~/.kimi-code/skills
python3 convert_to_kimi.py --dst ./skills --clean
python3 validate_skills.py ./skills
```

## Scope & authorization

Same as upstream: external attack surface only, for assets you own or have
written authorization to test (bug bounty scope, signed engagement letters,
CTF/practice platforms). See upstream [SECURITY.md](https://github.com/elementalsouls/Claude-BugHunter/blob/main/SECURITY.md).

---

## En español

Versión mirror de Claude-BugHunter para Kimi Code CLI, con bot de
sincronización diaria contra el repo original. Instalación: copiá `skills/`
a `~/.kimi-code/skills/`, reiniciá la sesión y describí tu objetivo en lenguaje
natural — la skill correcta se carga sola. Los comandos de engagement se
invocan con `/skill:cbh-<nombre>`.
