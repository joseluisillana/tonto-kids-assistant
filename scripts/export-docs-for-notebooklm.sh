#!/bin/bash
set -eEuo pipefail
exec 3>&2
exec 2>/dev/null

# Never emit raw paths or command errors when validation fails.
fail() {
  echo "NotebookLM export rejected: $1" >&3
  exit 1
}
trap 'fail "operation failed"' ERR

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)"
cd "$REPO_ROOT"
OUTPUT_PATH="${1:-exports/notebooklm}"
[[ "$OUTPUT_PATH" != *$'\n'* && "$OUTPUT_PATH" != *$'\r'* ]] || fail "invalid destination"
if [[ "$OUTPUT_PATH" != /* ]]; then OUTPUT_PATH="$REPO_ROOT/$OUTPUT_PATH"; fi
EXPORT_ROOT=$(realpath -ms -- "$OUTPUT_PATH" 2>/dev/null) || fail "invalid destination"
[[ "$EXPORT_ROOT" = "$REPO_ROOT/exports/"* ]] || fail "destination must be a subdirectory of exports"

# Check every existing component without following links, including broken ones.
check_path() {
  local relative="${1#"$REPO_ROOT/"}" component current="$REPO_ROOT"
  local -a components
  IFS=/ read -r -a components <<< "$relative"
  for component in "${components[@]}"; do
    current="$current/$component"
    [[ ! -L "$current" ]] || fail "symbolic links are not allowed"
  done
}
check_path "$EXPORT_ROOT"
[[ ! -e "$EXPORT_ROOT" || -d "$EXPORT_ROOT" ]] || fail "destination is not a directory"

# Validate trees before glob expansion, which could otherwise traverse a link.
for tree in docs specs; do
  check_path "$REPO_ROOT/$tree"
  if [[ -d "$tree" ]]; then
    links=$(find -P "$tree" -type l -print -quit 2>/dev/null) || fail "cannot validate sources"
    [[ -z "$links" ]] || fail "symbolic links are not allowed"
  fi
done
check_path "$REPO_ROOT/web"
shopt -s globstar nullglob
CANDIDATES=(README.md AGENTS.md docs/**/*.md specs/**/*.md web/README.md)
MD_FILES=()
for file in "${CANDIDATES[@]}"; do
  check_path "$REPO_ROOT/$file"
  [[ ! -e "$file" || -f "$file" ]] || fail "source is not a regular file"
  if [[ -f "$file" ]]; then
    [[ "$file" != *$'\n'* && "$file" != *$'\r'* ]] || fail "invalid source name"
    case "/$file" in
      */.env*|*/secrets/*|*/credentials*|*/.ssh/*|*/.aws/*|*/.codex/*|*/.agents/*|*.key.md|*.pem.md|*.p12.md|*.pfx.md)
        fail "protected source category" ;;
    esac
    link_count=$(stat -c %h -- "$file" 2>/dev/null) || fail "cannot validate source"
    [[ "$link_count" = 1 ]] || fail "hardlinked sources are not allowed"
    MD_FILES+=("$file")
  fi
done

PARENT=$(dirname -- "$EXPORT_ROOT")
mkdir -p -- "$PARENT" 2>/dev/null || fail "cannot prepare destination"
STAGING=$(mktemp -d "$PARENT/.notebooklm-stage-XXXXXX" 2>/dev/null) || fail "cannot prepare staging"
cleanup() { rm -rf -- "$STAGING" 2>/dev/null; }
trap cleanup EXIT
FINAL_ROOT="$EXPORT_ROOT"
EXPORT_ROOT="$STAGING"

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
    cp -- "$file" "$EXPORT_ROOT/$export_name" 2>/dev/null || fail "cannot copy source"
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
    cat -- "$file" >> "$COMBINED_FILE" 2>/dev/null || fail "cannot combine source"
  fi
done

# Replace only a validated derived-output directory; failed validation never deletes it.
check_path "$FINAL_ROOT"
BACKUP=""
if [[ -d "$FINAL_ROOT" ]]; then
  BACKUP=$(mktemp -d "$PARENT/.notebooklm-old-XXXXXX" 2>/dev/null) || fail "cannot preserve previous export"
  if ! mv -T -- "$FINAL_ROOT" "$BACKUP" 2>/dev/null; then
    rmdir -- "$BACKUP" 2>/dev/null || true
    fail "cannot preserve previous export"
  fi
fi
if ! mv -T -- "$STAGING" "$FINAL_ROOT" 2>/dev/null; then
  if [[ -n "$BACKUP" ]]; then mv -T -- "$BACKUP" "$FINAL_ROOT" 2>/dev/null || true; fi
  fail "cannot replace export; previous output preserved"
fi
if [[ -n "$BACKUP" ]]; then rm -rf -- "$BACKUP" 2>/dev/null || fail "cannot remove previous derived output"; fi
echo "Exported NotebookLM source files to $FINAL_ROOT"
