#!/usr/bin/env python3
"""Convierte el bundle Claude-BugHunter al formato de skills de Kimi Code.

Uso local:
    python3 convert_to_kimi.py
    python3 convert_to_kimi.py --src ~/github/Claude-BugHunter --dst ~/.kimi-code/skills

Uso CI (bot de sync):
    python3 convert_to_kimi.py --src /tmp/upstream --dst ./skills --clean
"""
import argparse
import re
import shutil
import sys
from pathlib import Path

import yaml

CMD_PREFIX = "cbh-"
ATTR = ("\n\n---\n*Adapted for Kimi Code from [Claude-BugHunter](https://github.com/elementalsouls/Claude-BugHunter) "
        "by Sachin Sharma / ElementalSoul — content CC BY 4.0.*\n")


def split_md(path: Path):
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not m:
        raise ValueError(f"frontmatter no encontrado: {path}")
    try:
        fm = yaml.safe_load(m.group(1))
    except yaml.YAMLError:
        # fallback tolerante: name/description de una sola línea,
        # valores que pueden traer ':' sin comillar (p.ej. 'Usage: /cmd x')
        name_m = re.search(r"^name:\s*(.+)$", m.group(1), re.M)
        desc_m = re.search(r"^description:\s*(.+)$", m.group(1), re.M)
        if not name_m or not desc_m:
            raise
        desc = desc_m.group(1).strip()
        if desc.startswith('"') and desc.endswith('"'):
            desc = desc[1:-1]
        fm = {"name": name_m.group(1).strip(), "description": desc}
    return fm, m.group(2)


def split_summary(desc: str) -> str:
    """Primera oración como resumen; tope 240 chars."""
    m = re.search(r"\.\s+(?=Use (?:when|at|for|before|after)\b)", desc, re.I)
    summary = desc[: m.end()].strip() if m else desc
    if len(summary) > 240:
        summary = summary[:237].rsplit(" ", 1)[0] + "..."
    return summary


def dump_fm(fields: dict) -> str:
    return yaml.safe_dump(fields, sort_keys=False, allow_unicode=True,
                          width=10**6, default_flow_style=False).strip()


def convert_skills(src: Path, dst: Path):
    ok, fail = [], []
    for skill_md in sorted(src.glob("skills/*/SKILL.md")):
        d = skill_md.parent
        try:
            fm, body = split_md(skill_md)
            name = fm["name"]
            desc = fm["description"].strip()
            new_fm = {
                "name": name,
                "description": split_summary(desc),
                "type": "prompt",
                "whenToUse": desc,
            }
            out_dir = dst / name
            out_dir.mkdir(parents=True, exist_ok=True)
            (out_dir / "SKILL.md").write_text(
                f"---\n{dump_fm(new_fm)}\n---\n{body.rstrip()}{ATTR}", encoding="utf-8")
            # archivos auxiliares
            for aux in d.iterdir():
                if aux.name == "SKILL.md":
                    continue
                tgt = out_dir / aux.name
                if aux.is_dir():
                    shutil.copytree(aux, tgt, dirs_exist_ok=True)
                else:
                    shutil.copy2(aux, tgt)
            ok.append(name)
        except Exception as e:  # noqa: BLE001
            fail.append(f"{d.name}: {e}")
    return ok, fail


def convert_commands(src: Path, dst: Path):
    ok, fail = [], []
    for cmd in sorted(src.glob("commands/*.md")):
        try:
            fm, body = split_md(cmd)
            name = f"{CMD_PREFIX}{fm['name']}"
            desc = fm["description"].strip()
            new_fm = {
                "name": name,
                "description": split_summary(desc),
                "type": "flow",
                "disableModelInvocation": True,
                "whenToUse": desc,
            }
            if "$TARGET" in body:
                new_fm["arguments"] = "target"
                body = body.replace("$TARGET", "$target")
            # colisiones con placeholders de Kimi dentro de bloques bash
            body = body.replace('TARGET="$1"', 'TARGET="$target"')
            body = body.replace("Cost:    Time: [X min], Capital: [$0 / $X]",
                                "Cost:    Time: [X min], Capital: [0 USD / X]")
            out_dir = dst / name
            out_dir.mkdir(parents=True, exist_ok=True)
            (out_dir / "SKILL.md").write_text(
                f"---\n{dump_fm(new_fm)}\n---\n{body.rstrip()}{ATTR}", encoding="utf-8")
            ok.append(name)
        except Exception as e:  # noqa: BLE001
            fail.append(f"{cmd.name}: {e}")
    return ok, fail


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--src", default=str(Path.home() / "github" / "Claude-BugHunter"),
                    help="clone del repo upstream (default: ~/github/Claude-BugHunter)")
    ap.add_argument("--dst", default=str(Path.home() / ".kimi-code" / "skills"),
                    help="directorio de skills destino (default: ~/.kimi-code/skills)")
    ap.add_argument("--clean", action="store_true",
                    help="borra el directorio destino antes de generar (solo para CI)")
    args = ap.parse_args()

    src, dst = Path(args.src), Path(args.dst)
    if not src.is_dir():
        print(f"ERROR: --src no existe: {src}", file=sys.stderr)
        return 2
    if args.clean and dst.exists():
        shutil.rmtree(dst)
    dst.mkdir(parents=True, exist_ok=True)

    s_ok, s_fail = convert_skills(src, dst)
    c_ok, c_fail = convert_commands(src, dst)
    print(f"skills convertidos:  {len(s_ok)}")
    print(f"comandos convertidos: {len(c_ok)}")
    for f in s_fail + c_fail:
        print(f"FALLO: {f}", file=sys.stderr)
    print(f"total en {dst}: {len(s_ok) + len(c_ok)}")
    return 1 if (s_fail or c_fail) else 0


if __name__ == "__main__":
    sys.exit(main())
