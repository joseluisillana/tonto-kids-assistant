import ast
import sys
from pathlib import Path

roots = [Path("backend"), Path("client"), Path("shared"), Path("tests")]
errors = []

for root in roots:
    if not root.exists():
        continue
    for path in root.rglob("*.py"):
        try:
            ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except SyntaxError as exc:
            errors.append(f"{path}: {exc}")

if errors:
    for error in errors:
        print(error, file=sys.stderr)
    sys.exit(1)

print("Python syntax OK")
