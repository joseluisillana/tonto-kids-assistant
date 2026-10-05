#!/bin/bash
set -eu

OUTPUT_PATH="${1:-exports/notebooklm}"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if [[ "$OUTPUT_PATH" = /* ]]; then
  EXPORT_ROOT="$OUTPUT_PATH"
else
  EXPORT_ROOT="$REPO_ROOT/$OUTPUT_PATH"
fi

if [[ "$EXPORT_ROOT" != "$REPO_ROOT"* ]]; then
  echo "Refusing to write outside repository: $EXPORT_ROOT" >&2
  exit 1
fi

if [ -d "$EXPORT_ROOT" ]; then
  rm -rf "$EXPORT_ROOT"
fi
mkdir -p "$EXPORT_ROOT"

shopt -s globstar nullglob
cd "$REPO_ROOT"
MD_FILES=(
  README.md
  AGENTS.md
  docs/**/*.md
  specs/**/*.md
  web/README.md
)

INDEX_FILE="$EXPORT_ROOT/INDEX.md"
COMBINED_FILE="$EXPORT_ROOT/NOTEBOOKLM_COMBINED.md"

cat << 'EOF' > "$INDEX_FILE"
# NotebookLM Source Export

Generated from repository documentation. This folder is derived output and is ignored by Git.

Use these files as NotebookLM sources, but keep final project documentation in the repository.

For routine NotebookLM refreshes, prefer `NOTEBOOKLM_COMBINED.md` so one source can be replaced instead of re-uploading many duplicated files.

## Sources

EOF

cat << 'EOF' > "$COMBINED_FILE"
# TONTO Kids Assistant - NotebookLM Combined Source

Generated from repository documentation. This file is derived output and is ignored by Git.

Use this single file as the primary NotebookLM source when you want to replace one document instead of re-importing many duplicated files.

Keep final project documentation in the repository. NotebookLM remains a reading and synthesis layer.

## Included Sources

EOF

for file in "${MD_FILES[@]}"; do
  if [ -f "$file" ]; then
    export_name="${file//\//__}"
    cp "$file" "$EXPORT_ROOT/$export_name"
    echo "- $export_name from $file" >> "$INDEX_FILE"
    echo "- \`$file\` exported as \`$export_name\`" >> "$COMBINED_FILE"
  fi
done

for file in "${MD_FILES[@]}"; do
  if [ -f "$file" ]; then
    echo "" >> "$COMBINED_FILE"
    echo "---" >> "$COMBINED_FILE"
    echo "" >> "$COMBINED_FILE"
    echo "## Source: $file" >> "$COMBINED_FILE"
    echo "" >> "$COMBINED_FILE"
    cat "$file" >> "$COMBINED_FILE"
  fi
done

echo "Exported NotebookLM source files to $EXPORT_ROOT"
