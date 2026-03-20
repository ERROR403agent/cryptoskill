#!/usr/bin/env bash
# Generate SOURCE.md attribution files for all skill directories.
set -euo pipefail

SKILLS_ROOT="/home/coder/github/cryptoskill/skills"

# Official/Likely-Official authors map: owner -> label
declare -A OFFICIAL_AUTHORS=(
  ["gate-exchange"]="Official Gate.io"
  ["nansen-devops"]="Official Nansen"
  ["ok-james-01"]="Official OKX"
  ["numpy0001"]="Likely-Official OKX"
  ["bryan-cmc"]="Official CoinMarketCap"
  ["roasbeef"]="Official Lightning Labs (CTO)"
  ["dfinzer"]="Official OpenSea (CEO)"
  ["0xmasayoshi"]="Likely-Official SushiSwap (CTO)"
  ["virtualstechteam"]="Official Virtuals Protocol"
  ["humanagent"]="Likely-Official XMTP"
  ["odilitime"]="Likely-Official ElizaOS"
  ["karryzhang"]="Likely-Official Bitget Wallet"
)

get_classification() {
  local owner="$1"
  if [[ -n "${OFFICIAL_AUTHORS[$owner]+_}" ]]; then
    echo "OFFICIAL (${OFFICIAL_AUTHORS[$owner]})"
  else
    echo "COMMUNITY"
  fi
}

count_with_meta=0
count_without_meta=0

for dir in "$SKILLS_ROOT"/*/*/; do
  # Strip trailing slash for basename
  dir="${dir%/}"
  dirname="$(basename "$dir")"
  category="$(basename "$(dirname "$dir")")"

  meta_file="$dir/_meta.json"
  source_file="$dir/SOURCE.md"

  if [[ -f "$meta_file" ]]; then
    # Extract owner and slug from _meta.json using python (available everywhere, handles JSON properly)
    owner=$(python3 -c "import json,sys; print(json.load(open(sys.argv[1]))['owner'])" "$meta_file")
    slug=$(python3 -c "import json,sys; print(json.load(open(sys.argv[1]))['slug'])" "$meta_file")

    classification=$(get_classification "$owner")

    cat > "$source_file" <<SOURCEEOF
# Source Attribution

- **Original Author**: ${owner}
- **Original Slug**: ${slug}
- **Source**: [ClawHub](https://clawhub.ai/skills/${owner}/${slug})
- **License**: MIT-0 (as per ClawHub publishing terms)
- **Classification**: ${classification}
SOURCEEOF

    count_with_meta=$((count_with_meta + 1))
  else
    # No _meta.json — use directory name as slug, mark author unknown
    cat > "$source_file" <<SOURCEEOF
# Source Attribution

- **Original Author**: Unknown
- **Original Slug**: ${dirname}
- **Source**: Unknown (no _meta.json found)
- **License**: MIT-0 (as per ClawHub publishing terms)
- **Classification**: COMMUNITY
SOURCEEOF

    count_without_meta=$((count_without_meta + 1))
  fi
done

echo "Done. Created SOURCE.md for ${count_with_meta} skills with _meta.json and ${count_without_meta} skills without."
