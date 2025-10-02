#!/usr/bin/env bash
set -euo pipefail

# ========= SCOPE CONFIG (edit here if needed) =========
DOCS_DIR="docs"
LIMIT_VOLUME="volume-1"   # only affect docs/volume-1
# You can set multiple scopes later by editing the Python script or passing multiple --limit-dirs
# =====================================================

REPO_ROOT="$(git rev-parse --show-toplevel)"
HOOK="$REPO_ROOT/.git/hooks/pre-commit"
SCRIPT="$REPO_ROOT/utilities/update_links_and_menus.py"
SCOPE_DIR="$REPO_ROOT/$DOCS_DIR/$LIMIT_VOLUME"

if [ ! -f "$SCRIPT" ]; then
  echo "[ERROR] script not found: $SCRIPT" >&2
  exit 1
fi

cat > "$HOOK" <<'HOOK'
#!/usr/bin/env bash
set -euo pipefail

# ========= SCOPE CONFIG (keep in sync with installer) =========
DOCS_DIR="docs"
LIMIT_VOLUME="volume-1"
# =============================================================

REPO_ROOT="$(git rev-parse --show-toplevel)"
SCRIPT="$REPO_ROOT/utilities/update_links_and_menus.py"
SCOPE_DIR="$REPO_ROOT/$DOCS_DIR/$LIMIT_VOLUME"

# Collect scoped staged Markdown files (added/copied/modified), NUL-delimited and safe
STAGED_MD_ARR=()
# Use :(glob) to support ** in pathspec
while IFS= read -r -d '' f; do
  STAGED_MD_ARR+=("$f")
done < <(git diff --cached --name-only --diff-filter=ACM -z -- ":(glob)$DOCS_DIR/$LIMIT_VOLUME/**/*.md" "$DOCS_DIR/$LIMIT_VOLUME/*.md")

if [ ${#STAGED_MD_ARR[@]} -eq 0 ]; then
  # Nothing staged in scope; still run within scope so it can create missing index.md etc.
  python3 "$SCRIPT" --docs-dir "$REPO_ROOT/$DOCS_DIR" --limit-dirs "$DOCS_DIR/$LIMIT_VOLUME" || {
    echo "[ERROR] fix script failed" >&2
    exit 1
  }
else
  # Run only on staged files (script will still auto-create missing index.md within scope)
  python3 "$SCRIPT" --docs-dir "$REPO_ROOT/$DOCS_DIR" --limit-dirs "$DOCS_DIR/$LIMIT_VOLUME" --paths "${STAGED_MD_ARR[@]}" || {
    echo "[ERROR] fix script failed" >&2
    exit 1
  }
fi

# Add newly created index.md (untracked) inside scope, NUL-safe
NEW_INDEX_ARR=()
while IFS= read -r -d '' f; do
  NEW_INDEX_ARR+=("$f")
done < <(git ls-files --others --exclude-standard -z -- "$DOCS_DIR/$LIMIT_VOLUME" -o -- ":(glob)$DOCS_DIR/$LIMIT_VOLUME/**/index.md")

if [ ${#NEW_INDEX_ARR[@]} -gt 0 ]; then
  git add -- "${NEW_INDEX_ARR[@]}"
fi

# Re-add modified Markdown files inside scope, NUL-safe
MODIFIED_MD_ARR=()
while IFS= read -r -d '' f; do
  MODIFIED_MD_ARR+=("$f")
done < <(git ls-files -m -z -- ":(glob)$DOCS_DIR/$LIMIT_VOLUME/**/*.md" "$DOCS_DIR/$LIMIT_VOLUME/*.md")

if [ ${#MODIFIED_MD_ARR[@]} -gt 0 ]; then
  git add -- "${MODIFIED_MD_ARR[@]}"
fi
HOOK

chmod +x "$HOOK"
echo "[OK] pre-commit hook installed at .git/hooks/pre-commit (scope: $DOCS_DIR/$LIMIT_VOLUME)"
