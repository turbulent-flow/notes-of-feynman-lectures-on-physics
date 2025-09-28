#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel)"
HOOK="$REPO_ROOT/.git/hooks/pre-commit"
SCRIPT="$REPO_ROOT/utilities/update_links_and_menus.py"

if [ ! -f "$SCRIPT" ]; then
  echo "[ERROR] script not found: $SCRIPT" >&2
  exit 1
fi

cat > "$HOOK" <<'HOOK'
#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel)"
SCRIPT="$REPO_ROOT/utilities/update_links_and_menus.py"

# Collect staged Markdown files (added/copied/modified), NUL-delimited and safe
STAGED_MD_ARR=()
while IFS= read -r -d '' f; do
  STAGED_MD_ARR+=("$f")
done < <(git diff --cached --name-only --diff-filter=ACM -z -- "*.md")

if [ ${#STAGED_MD_ARR[@]} -eq 0 ]; then
  # Nothing staged specifically; still run globally so it can create missing index.md etc.
  python3 "$SCRIPT" --docs-dir "$REPO_ROOT/docs" || {
    echo "[ERROR] fix script failed" >&2
    exit 1
  }
else
  # Run only on staged files (script will still auto-create missing index.md)
  python3 "$SCRIPT" --paths "${STAGED_MD_ARR[@]}" || {
    echo "[ERROR] fix script failed" >&2
    exit 1
  }
fi

# Add newly created index.md (untracked), NUL-safe
NEW_INDEX_ARR=()
while IFS= read -r -d '' f; do
  NEW_INDEX_ARR+=("$f")
done < <(git ls-files --others --exclude-standard -z -- 'docs/volume-*/**/index.md')

if [ ${#NEW_INDEX_ARR[@]} -gt 0 ]; then
  git add -- "${NEW_INDEX_ARR[@]}"
fi

# Re-add modified Markdown files to index, NUL-safe
MODIFIED_MD_ARR=()
while IFS= read -r -d '' f; do
  MODIFIED_MD_ARR+=("$f")
done < <(git ls-files -m -z -- "*.md")

if [ ${#MODIFIED_MD_ARR[@]} -gt 0 ]; then
  git add -- "${MODIFIED_MD_ARR[@]}"
fi
HOOK

chmod +x "$HOOK"
echo "[OK] pre-commit hook installed at .git/hooks/pre-commit"
