#!/usr/bin/env python3
"""CryptoSkill Auto-Update Bot

Scans the OpenClaw skills repository for new crypto-related skills,
copies them into the CryptoSkill registry, and updates the website.
"""

import argparse
import json
import logging
import os
import re
import shutil
import subprocess
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / "skills"
DOCS_DIR = REPO_ROOT / "docs"
SKILLS_JSON = DOCS_DIR / "skills.json"
INDEX_HTML = DOCS_DIR / "index.html"

# How far back (in days) to consider a skill "new"
LOOKBACK_DAYS = 7

# Crypto keyword buckets used for both detection and categorisation
KEYWORDS = {
    "exchanges": [
        "binance", "okx", "coinbase", "kraken", "bybit", "gate", "bitget",
        "kucoin", "mexc", "hyperliquid",
    ],
    "chains": [
        "ethereum", "solana", "bitcoin", "polygon", "arbitrum", "base", "sui",
        "aptos", "monad", "ton", "near", "tron", "starknet", "zksync",
    ],
    "defi": [
        "defi", "swap", "uniswap", "aave", "lido", "compound", "makerdao",
        "curve", "pancakeswap", "raydium", "jupiter", "pump",
    ],
    "trading": [
        "trading", "bot", "signal",
    ],
    "analytics": [
        "dune", "coingecko", "coinmarketcap", "etherscan", "nansen",
        "defillama", "thegraph", "zapper", "zerion",
    ],
    "wallets": [
        "wallet",
    ],
    "payments": [
        "x402", "payment",
    ],
    "prediction-markets": [
        "polymarket", "prediction",
    ],
    "social": [
        "farcaster", "nostr", "social",
    ],
    "ai-crypto": [
        "bittensor", "virtuals", "eliza", "ai-agent",
    ],
    "identity": [
        "8004", "erc-8004", "identity",
    ],
    "mcp-servers": [
        "mcp server", "mcp-server",
    ],
}

# Flat list of every keyword (used for the initial crypto-relevance check)
ALL_CRYPTO_KEYWORDS = (
    KEYWORDS["exchanges"]
    + KEYWORDS["chains"]
    + KEYWORDS["defi"]
    + KEYWORDS["trading"]
    + KEYWORDS["analytics"]
    + KEYWORDS["wallets"]
    + KEYWORDS["payments"]
    + KEYWORDS["prediction-markets"]
    + KEYWORDS["social"]
    + KEYWORDS["ai-crypto"]
    + KEYWORDS["identity"]
    + KEYWORDS["mcp-servers"]
    + [
        "crypto", "blockchain", "token", "nft", "staking", "yield",
        "lending", "bridge", "oracle", "mev",
        "moralis", "alchemy", "foundry", "hardhat", "wagmi", "viem", "mcp",
    ]
)

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger("auto-update")

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def read_json(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def write_json(path: Path, data: dict) -> None:
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2, ensure_ascii=False)
        fh.write("\n")


def parse_skill_md_frontmatter(path: Path) -> dict:
    """Return the YAML front-matter from a SKILL.md as a dict."""
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return {}
    m = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if not m:
        return {}
    # Minimal YAML-ish parser (avoids pyyaml dependency)
    fm: dict = {}
    current_list_key = None
    for line in m.group(1).splitlines():
        # list item
        list_match = re.match(r"^\s+-\s+(.+)", line)
        if list_match and current_list_key:
            fm.setdefault(current_list_key, []).append(
                list_match.group(1).strip().strip('"').strip("'")
            )
            continue
        # key: value
        kv = re.match(r"^(\w[\w-]*):\s*(.*)", line)
        if kv:
            key = kv.group(1)
            val = kv.group(2).strip().strip('"').strip("'")
            if val:
                fm[key] = val
                current_list_key = None
            else:
                current_list_key = key
            continue
        current_list_key = None
    return fm


def text_matches_keywords(text: str, keywords: list[str]) -> bool:
    """Case-insensitive check: does *text* contain any of *keywords*?"""
    lower = text.lower()
    return any(kw in lower for kw in keywords)


def categorize_skill(name: str, description: str) -> str:
    """Pick the best category for a skill based on its name+description."""
    blob = f"{name} {description}".lower()
    # Check in priority order
    priority = [
        "exchanges", "prediction-markets", "payments", "identity",
        "social", "ai-crypto", "mcp-servers", "chains", "defi",
        "analytics", "wallets", "trading",
    ]
    for cat in priority:
        if any(kw in blob for kw in KEYWORDS[cat]):
            return cat
    return "dev-tools"


def existing_skill_names() -> set[str]:
    """Return set of skill directory names already in the repo."""
    names: set[str] = set()
    for cat_dir in SKILLS_DIR.iterdir():
        if not cat_dir.is_dir():
            continue
        for skill_dir in cat_dir.iterdir():
            if skill_dir.is_dir():
                names.add(skill_dir.name)
    return names


def generate_source_md(owner: str, slug: str) -> str:
    return (
        "# Source Attribution\n"
        "\n"
        f"- **Original Author**: {owner}\n"
        f"- **Original Slug**: {slug}\n"
        f"- **Source**: [ClawHub](https://clawhub.ai/skills/{owner}/{slug})\n"
        "- **License**: MIT-0 (as per ClawHub publishing terms)\n"
        "- **Classification**: COMMUNITY\n"
    )


def make_display_name(slug: str) -> str:
    """Convert 'binance-spot-api' -> 'Binance Spot Api'."""
    return " ".join(w.capitalize() for w in slug.split("-"))


# ---------------------------------------------------------------------------
# Core logic
# ---------------------------------------------------------------------------


def find_new_crypto_skills(source_dir: Path, lookback_days: int) -> list[dict]:
    """Walk the source skills repo and return list of new crypto skills."""
    cutoff_ms = int(
        (datetime.now(timezone.utc) - timedelta(days=lookback_days)).timestamp() * 1000
    )
    new_skills: list[dict] = []
    existing = existing_skill_names()

    if not source_dir.is_dir():
        log.error("Source directory does not exist: %s", source_dir)
        return []

    for owner_dir in sorted(source_dir.iterdir()):
        if not owner_dir.is_dir():
            continue
        for skill_dir in sorted(owner_dir.iterdir()):
            if not skill_dir.is_dir():
                continue

            meta_path = skill_dir / "_meta.json"
            skill_md_path = skill_dir / "SKILL.md"
            if not meta_path.exists():
                continue

            try:
                meta = read_json(meta_path)
            except (json.JSONDecodeError, OSError):
                log.warning("Skipping %s – bad _meta.json", skill_dir)
                continue

            slug = meta.get("slug", skill_dir.name)

            # Already in repo?
            if slug in existing:
                continue

            # Published recently?
            published_at = meta.get("latest", {}).get("publishedAt", 0)
            if published_at < cutoff_ms:
                continue

            # Read SKILL.md for description
            fm = {}
            if skill_md_path.exists():
                fm = parse_skill_md_frontmatter(skill_md_path)

            name = fm.get("name", slug)
            description = fm.get("description", meta.get("displayName", slug))

            # Crypto relevant?
            blob = f"{name} {description} {' '.join(fm.get('tags', []))}".lower()
            if not text_matches_keywords(blob, ALL_CRYPTO_KEYWORDS):
                continue

            category = categorize_skill(name, description)

            new_skills.append(
                {
                    "slug": slug,
                    "name": name,
                    "displayName": meta.get("displayName", make_display_name(slug)),
                    "description": description,
                    "category": category,
                    "tags": fm.get("tags", []),
                    "author": meta.get("owner", fm.get("author", "unknown")),
                    "version": meta.get("latest", {}).get("version", fm.get("version", "1.0.0")),
                    "owner": meta.get("owner", "unknown"),
                    "source_path": str(skill_dir),
                }
            )
            log.info(
                "Found new skill: %s -> %s (published %s)",
                slug,
                category,
                datetime.fromtimestamp(published_at / 1000, tz=timezone.utc).strftime(
                    "%Y-%m-%d"
                ),
            )

    return new_skills


def copy_skills(skills: list[dict], dry_run: bool = False) -> int:
    """Copy skill directories into the appropriate category folders."""
    copied = 0
    for skill in skills:
        src = Path(skill["source_path"])
        dst = SKILLS_DIR / skill["category"] / skill["slug"]

        if dst.exists():
            log.info("Skipping %s – already exists at %s", skill["slug"], dst)
            continue

        if dry_run:
            log.info("[DRY-RUN] Would copy %s -> %s", src, dst)
            copied += 1
            continue

        # Ensure category dir exists
        dst.parent.mkdir(parents=True, exist_ok=True)

        shutil.copytree(src, dst)

        # Write SOURCE.md
        source_md = dst / "SOURCE.md"
        source_md.write_text(
            generate_source_md(skill["owner"], skill["slug"]),
            encoding="utf-8",
        )

        log.info("Copied %s -> %s", skill["slug"], dst)
        copied += 1

    return copied


def update_skills_json(skills: list[dict], dry_run: bool = False) -> None:
    """Add new skills to docs/skills.json."""
    if not SKILLS_JSON.exists():
        log.warning("skills.json not found at %s", SKILLS_JSON)
        return

    catalog = read_json(SKILLS_JSON)
    existing_names = {s["name"] for s in catalog.get("skills", [])}

    added = 0
    for skill in skills:
        if skill["slug"] in existing_names:
            continue

        entry = {
            "name": skill["slug"],
            "displayName": skill["displayName"],
            "description": skill["description"],
            "category": skill["category"],
            "tags": skill["tags"] if skill["tags"] else [skill["category"]],
            "author": skill["author"],
            "version": skill["version"],
        }
        catalog["skills"].append(entry)
        added += 1

    if added == 0:
        log.info("No new entries to add to skills.json")
        return

    if dry_run:
        log.info("[DRY-RUN] Would add %d entries to skills.json", added)
        return

    write_json(SKILLS_JSON, catalog)
    log.info("Added %d entries to skills.json (total: %d)", added, len(catalog["skills"]))


def update_index_html(dry_run: bool = False) -> None:
    """Update the skill count stat in docs/index.html."""
    if not INDEX_HTML.exists():
        log.warning("index.html not found at %s", INDEX_HTML)
        return

    # Count skills
    total = 0
    categories = 0
    for cat_dir in sorted(SKILLS_DIR.iterdir()):
        if not cat_dir.is_dir():
            continue
        cat_count = sum(1 for d in cat_dir.iterdir() if d.is_dir())
        if cat_count > 0:
            categories += 1
            total += cat_count

    html = INDEX_HTML.read_text(encoding="utf-8")

    # Update skill count — matches patterns like "310+" or "315+"
    new_stat = f"{total}+"
    html = re.sub(
        r'(<div class="stat-value" id="statSkills">)\d+\+?(</div>)',
        rf"\g<1>{new_stat}\2",
        html,
    )
    # Update category count
    html = re.sub(
        r'(<div class="stat-value" id="statCategories">)\d+(</div>)',
        rf"\g<1>{categories}\2",
        html,
    )
    # Update "310+" mentions in descriptive text
    html = re.sub(
        r'(\b)\d{2,4}\+(\s*(?:crypto )?skills)',
        rf"\g<1>{new_stat}\2",
        html,
    )

    if dry_run:
        log.info("[DRY-RUN] Would update index.html: %d skills, %d categories", total, categories)
        return

    INDEX_HTML.write_text(html, encoding="utf-8")
    log.info("Updated index.html: %d skills, %d categories", total, categories)


def git_commit_and_push(count: int, dry_run: bool = False) -> None:
    """Stage, commit, and push changes."""
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    message = f"Auto-update: add {count} new crypto skills ({today})"

    if dry_run:
        log.info("[DRY-RUN] Would commit: %s", message)
        return

    try:
        subprocess.run(["git", "add", "-A"], cwd=REPO_ROOT, check=True)
        # Check if there are staged changes
        result = subprocess.run(
            ["git", "diff", "--cached", "--quiet"],
            cwd=REPO_ROOT,
            capture_output=True,
        )
        if result.returncode == 0:
            log.info("No changes to commit")
            return

        subprocess.run(
            ["git", "commit", "-m", message],
            cwd=REPO_ROOT,
            check=True,
        )
        log.info("Committed: %s", message)

        subprocess.run(["git", "push"], cwd=REPO_ROOT, check=True)
        log.info("Pushed to remote")
    except subprocess.CalledProcessError as exc:
        log.error("Git operation failed: %s", exc)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Auto-discover and import new crypto skills from the OpenClaw skills repo."
    )
    parser.add_argument(
        "--source-dir",
        type=Path,
        default=REPO_ROOT.parent / "skills" / "skills",
        help="Path to the OpenClaw skills/skills/ directory (default: ../skills/skills)",
    )
    parser.add_argument(
        "--lookback-days",
        type=int,
        default=LOOKBACK_DAYS,
        help=f"Number of days to look back for new skills (default: {LOOKBACK_DAYS})",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without modifying anything",
    )
    parser.add_argument(
        "--no-push",
        action="store_true",
        help="Commit but do not push to remote",
    )
    args = parser.parse_args()

    if args.dry_run:
        log.info("=== DRY-RUN MODE ===")

    log.info("Source directory: %s", args.source_dir)
    log.info("Looking back %d days", args.lookback_days)

    # 1. Find new crypto skills
    new_skills = find_new_crypto_skills(args.source_dir, args.lookback_days)
    if not new_skills:
        log.info("No new crypto skills found — nothing to do.")
        return

    log.info("Found %d new crypto skill(s)", len(new_skills))

    # 2. Copy skills into repo
    copied = copy_skills(new_skills, dry_run=args.dry_run)

    # 3. Update skills.json
    update_skills_json(new_skills, dry_run=args.dry_run)

    # 4. Update index.html stats
    update_index_html(dry_run=args.dry_run)

    # 5. Git commit & push
    if not args.dry_run:
        if args.no_push:
            # Just commit, skip push
            today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
            message = f"Auto-update: add {copied} new crypto skills ({today})"
            try:
                subprocess.run(["git", "add", "-A"], cwd=REPO_ROOT, check=True)
                result = subprocess.run(
                    ["git", "diff", "--cached", "--quiet"],
                    cwd=REPO_ROOT,
                    capture_output=True,
                )
                if result.returncode != 0:
                    subprocess.run(
                        ["git", "commit", "-m", message],
                        cwd=REPO_ROOT,
                        check=True,
                    )
                    log.info("Committed: %s (push skipped)", message)
                else:
                    log.info("No changes to commit")
            except subprocess.CalledProcessError as exc:
                log.error("Git operation failed: %s", exc)
        else:
            git_commit_and_push(copied, dry_run=args.dry_run)

    log.info("Done! %d skill(s) processed.", copied)


if __name__ == "__main__":
    main()
