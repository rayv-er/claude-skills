#!/bin/bash

# Skills installer for ~/.claude/skills/
# Idempotent -- safe to re-run. Uses symlinks so edits propagate automatically.
# Backs up existing entries before overwriting.

set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_TARGET="$HOME/.claude/skills"
BACKUP_DIR="$HOME/.dotfiles_backup/$(date +%Y%m%d_%H%M%S)"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

LINKED=0
SKIPPED=0
BACKED_UP=0

log_link()   { echo -e "${GREEN}  + linked${NC}  $1 -> $2"; ((LINKED++)) || true; }
log_skip()   { echo -e "${YELLOW}  - skipped${NC} $1 ($2)"; ((SKIPPED++)) || true; }
log_backup() { echo -e "${BLUE}  ~ backup${NC}  $1 -> $BACKUP_DIR/"; ((BACKED_UP++)) || true; }

link_file() {
    local src="$1"
    local dst="$2"

    if [ ! -e "$src" ]; then
        log_skip "$dst" "source missing: $src"
        return
    fi

    mkdir -p "$(dirname "$dst")"

    if [ -L "$dst" ] && [ "$(readlink "$dst")" = "$src" ]; then
        log_skip "$dst" "already linked"
        return
    fi

    if [ -e "$dst" ] || [ -L "$dst" ]; then
        mkdir -p "$BACKUP_DIR"
        log_backup "$dst"
        mv "$dst" "$BACKUP_DIR/$(basename "$dst").$(basename "$(dirname "$dst")")"
    fi

    ln -sf "$src" "$dst"
    log_link "$dst" "$src"
}

echo ""
echo -e "${BLUE}claude-skills installer${NC}  ($(date))"
echo -e "${BLUE}Source:${NC}  $REPO_DIR/skills"
echo -e "${BLUE}Target:${NC}  $SKILLS_TARGET"
echo ""

mkdir -p "$SKILLS_TARGET"

echo -e "${BLUE}[skills]${NC}"
for skill_dir in "$REPO_DIR/skills"/*/; do
    [ -d "$skill_dir" ] || continue
    skill_name="$(basename "$skill_dir")"
    link_file "$skill_dir" "$SKILLS_TARGET/$skill_name"
done
echo ""

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}  Linked:${NC}    $LINKED"
echo -e "${YELLOW}  Skipped:${NC}   $SKIPPED"
echo -e "${BLUE}  Backed up:${NC} $BACKED_UP"
if [ "$BACKED_UP" -gt 0 ]; then
    echo -e "${BLUE}  Backups in:${NC} $BACKUP_DIR"
fi
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
