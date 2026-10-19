#!/usr/bin/env python3
"""Valida skills en formato Kimi Code. Sale con código 1 si hay errores.

Uso:
    python3 validate_skills.py [directorio_skills]   (default: ./skills)

Chequeos:
  - cada subdirectorio tiene un SKILL.md parseable (YAML frontmatter)
  - name y description presentes; whenToUse presente
  - name coincide con el nombre del directorio
  - sin nombres duplicados
"""
import re
import sys
from pathlib import Path

import yaml


def validate(root: Path):
    errors, names, seen_when = [], [], 0
    if not root.is_dir():
        return [f"directorio inexistente: {root}"], [], 0
    dirs = sorted(d for d in root.iterdir() if d.is_dir())
    if not dirs:
        return [f"sin skills en {root}"], [], 0
    for d in dirs:
        f = d / "SKILL.md"
        if not f.exists():
            errors.append(f"{d.name}: sin SKILL.md")
            continue
        m = re.match(r"^---\n(.*?)\n---\n", f.read_text(encoding="utf-8"), re.S)
        if not m:
            errors.append(f"{d.name}: frontmatter roto (sin ---)")
            continue
        try:
            fm = yaml.safe_load(m.group(1))
        except yaml.YAMLError as e:
            errors.append(f"{d.name}: YAML inválido: {e}")
            continue
        if not isinstance(fm, dict):
            errors.append(f"{d.name}: frontmatter no es un mapping")
            continue
        if not fm.get("name"):
            errors.append(f"{d.name}: falta 'name'")
        if not fm.get("description"):
            errors.append(f"{d.name}: falta 'description'")
        if not fm.get("whenToUse"):
            errors.append(f"{d.name}: falta 'whenToUse'")
        if fm.get("name") and fm["name"] != d.name:
            errors.append(f"{d.name}: name '{fm['name']}' != directorio")
        names.append(fm.get("name") or d.name)
        seen_when += 1 if fm.get("whenToUse") else 0
    dupes = sorted({n for n in names if names.count(n) > 1})
    for n in dupes:
        errors.append(f"nombre duplicado: {n}")
    return errors, names, seen_when


def main():
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("skills")
    errors, names, _ = validate(root)
    print(f"validados: {len(names)} skills en {root}")
    if errors:
        print(f"errores: {len(errors)}")
        for e in errors:
            print(f"  - {e}")
        return 1
    print("OK: sin errores")
    return 0


if __name__ == "__main__":
    sys.exit(main())
