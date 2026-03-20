<div align="center">

# CryptoSkill

**The Crypto Skill Hub for AI Agents**

Discover, install, and build AI agent skills for every crypto protocol, exchange, and tool.

[![Skills](https://img.shields.io/badge/skills-409-6366f1)]() [![MCP Servers](https://img.shields.io/badge/MCP%20servers-38-f59e0b)]() [![Categories](https://img.shields.io/badge/categories-13-22d3ee)]() [![License](https://img.shields.io/badge/license-AGPL--3.0-green)]()

[Website](https://cryptoskill.app) · [Browse Skills](#skills-overview) · [MCP Servers](#mcp-servers) · [Submit a Skill](#submit-a-skill) · [Contributing](CONTRIBUTING.md)

</div>

---

## What is CryptoSkill?

CryptoSkill is a curated registry of AI agent skills and MCP servers for the crypto ecosystem. Each skill is a self-contained module that teaches an AI agent how to interact with a specific protocol, exchange, or tool -- from placing trades on Binance to monitoring DeFi positions on Aave.

Whether you're building an autonomous trading agent, a portfolio tracker, or a research assistant, CryptoSkill gives you production-ready building blocks so you don't have to start from scratch.

### Why CryptoSkill?

- **409 skills** covering the full crypto stack -- exchanges, DeFi, wallets, analytics, and more
- **38 MCP servers** for direct protocol integration with Claude, Cursor, and other AI tools
- **Official skills** from verified project teams (Binance, OKX, Coinbase, Gate.io, Kraken, KuCoin, Uniswap, Nansen, and more)
- **Plug and play** -- each skill follows a standard format compatible with [OpenClaw](https://github.com/nicholasgriffintn/openclaw) agents
- **Always growing** -- new skills and MCP servers are added regularly as the ecosystem evolves

## Skills Overview

| Category | Skills | Highlights |
|---|---|---|
| **Exchanges** | 167 | Binance (official), OKX (official), Gate.io (official), Bitget (official), Kraken (official), KuCoin (official), Hyperliquid, Bybit, Coinbase, MEXC |
| **Chains** | 41 | Ethereum, Solana, Bitcoin, Lightning Network, Arbitrum, Base, Sui, Polygon, Cosmos, Monad, TON |
| **MCP Servers** | 38 | Coinbase AgentKit, Alchemy, Solana Agent Kit, GOAT, Tatum, deBridge, Kraken CLI, Jupiter, Helius, DeFi Llama |
| **Analytics** | 34 | CoinMarketCap (official), CoinGecko, Nansen (official), DefiLlama, Dune, Etherscan, The Graph, Zapper, Zerion |
| **DeFi** | 29 | Uniswap (official), Aave, SushiSwap, PancakeSwap, Raydium, OpenSea (official), Pump.fun, Jupiter |
| **Trading** | 25 | Grid trading, copy trading, whale tracking, yield scanning, airdrop hunting, signals |
| **Identity** | 14 | ERC-8004 on-chain agent identity, discovery, reputation, Pinata |
| **Payments** | 13 | x402 protocol, agent marketplace, paywall kit, private search |
| **Wallets** | 13 | MetaMask, Bitget Wallet (official), Cobo TSS, WalletConnect, MPC payments |
| **Prediction Markets** | 12 | Polymarket trading, odds, data API, whale copying, sports edge |
| **Dev Tools** | 11 | Alchemy (official MCP), Moralis, Foundry, Hardhat, Viem, Wagmi |
| **Social** | 7 | Farcaster, Nostr, XMTP (official) |
| **AI x Crypto** | 5 | Bittensor, Virtuals Protocol (official), ElizaOS |

## MCP Servers

CryptoSkill maintains a collection of **38 MCP (Model Context Protocol) servers** for crypto -- the largest curated list focused on the crypto ecosystem. MCP servers provide direct tool integration with AI assistants like Claude, Cursor, and Codex.

| MCP Server | Description |
|---|---|
| [Alchemy MCP](skills/mcp-servers/alchemy-mcp/) | Multi-chain RPC, NFT, and token APIs |
| [Algorand MCP](skills/mcp-servers/algorand-mcp/) | Algorand blockchain interaction |
| [Alby NWC MCP](skills/mcp-servers/alby-nwc-mcp/) | Lightning Network wallet connect |
| [Aptos MCP](skills/mcp-servers/aptos-mcp/) | Aptos blockchain tools |
| [Base MCP](skills/mcp-servers/base-mcp/) | Base L2 chain integration |
| [Bitcoin MCP](skills/mcp-servers/bitcoin-mcp/) | Bitcoin network tools |
| [Blockscout MCP](skills/mcp-servers/blockscout-mcp/) | Block explorer API access |
| [BNB Chain MCP](skills/mcp-servers/bnbchain-mcp/) | BNB Chain integration |
| [CCXT MCP](skills/mcp-servers/ccxt-mcp/) | Unified exchange API (100+ exchanges) |
| [Chainlink Feeds MCP](skills/mcp-servers/chainlink-feeds-mcp/) | Chainlink price feed data |
| [Coinbase AgentKit](skills/mcp-servers/coinbase-agentkit/) | Coinbase wallet and trading |
| [CoinGecko MCP](skills/mcp-servers/coingecko-mcp-official/) | Market data and token info |
| [CoinStats MCP](skills/mcp-servers/coinstats-mcp/) | Portfolio and market tracking |
| [deBridge MCP](skills/mcp-servers/debridge-mcp/) | Cross-chain bridging |
| [DeFi Llama MCP](skills/mcp-servers/defillama-mcp/) | TVL and DeFi analytics |
| [DexPaprika MCP](skills/mcp-servers/dexpaprika-mcp/) | DEX data aggregation |
| [DEXScreener MCP](skills/mcp-servers/dexscreener-mcp/) | Real-time DEX pair tracking |
| [Dune Analytics MCP](skills/mcp-servers/dune-analytics-mcp/) | On-chain analytics queries |
| [EVM MCP](skills/mcp-servers/evm-mcp/) | Generic EVM chain tools |
| [Funding Rates MCP](skills/mcp-servers/funding-rates-mcp/) | Perpetual funding rate data |
| [GOAT Onchain](skills/mcp-servers/goat-onchain/) | Multi-chain transaction toolkit |
| [Helius MCP](skills/mcp-servers/helius-mcp/) | Solana RPC and DAS API |
| [Hive Crypto MCP](skills/mcp-servers/hive-crypto-mcp/) | Hive blockchain integration |
| [Jupiter MCP](skills/mcp-servers/jupiter-mcp/) | Solana swap aggregation |
| [Kraken CLI MCP](skills/mcp-servers/kraken-cli-mcp/) | Kraken exchange CLI tools |
| [LI.FI MCP](skills/mcp-servers/lifi-mcp/) | Cross-chain swap and bridge aggregator |
| [Lightning MCP](skills/mcp-servers/lightning-mcp/) | Lightning Network payments |
| [Monad MCP](skills/mcp-servers/monad-mcp/) | Monad blockchain tools |
| [NEAR MCP](skills/mcp-servers/near-mcp/) | NEAR protocol integration |
| [Nodit MCP](skills/mcp-servers/nodit-mcp/) | Multi-chain node infrastructure |
| [Solana Agent Kit](skills/mcp-servers/solana-agent-kit/) | Full Solana agent toolkit |
| [Solana Dev MCP](skills/mcp-servers/solana-dev-mcp/) | Solana developer tools |
| [Solana MCP](skills/mcp-servers/solana-mcp-official/) | Official Solana MCP server |
| [StarkNet MCP](skills/mcp-servers/starknet-mcp/) | StarkNet L2 integration |
| [Tatum Blockchain MCP](skills/mcp-servers/tatum-blockchain-mcp/) | Multi-chain API platform |
| [The Graph Token API](skills/mcp-servers/thegraph-token-api/) | Subgraph token data |
| [Web3 MCP](skills/mcp-servers/web3-mcp/) | General Web3 integration tools |
| [Whale Tracker MCP](skills/mcp-servers/whale-tracker-mcp/) | Large transaction monitoring |

> **Looking for an MCP server that's not listed?** [Submit it!](#submit-a-skill)

## Quick Start

### Browse Skills

Visit [cryptoskill.app](https://cryptoskill.app) to search and browse all skills with filtering by category, protocol, and use case.

### Install a Skill

Each skill is a directory containing a `SKILL.md` (documentation and frontmatter) and `_meta.json` (metadata). To use a skill with an OpenClaw-compatible agent:

```bash
# Clone the repository
git clone https://github.com/jiayaoqijia/cryptoskill.git
cd cryptoskill

# Copy a skill into your agent's workspace
cp -r skills/exchanges/binance-spot-api ~/my-agent/workspace/skills/
```

### Skill Format

Every skill follows a standard structure:

```
skills/{category}/{skill-name}/
  SKILL.md        # Frontmatter + documentation
  _meta.json      # Version history and ownership
  SOURCE.md       # Attribution and provenance
  index.js        # Optional: executable entry point
  skill.yaml      # Optional: additional configuration
  scripts/        # Optional: executable scripts
  references/     # Optional: reference documentation
```

The `SKILL.md` frontmatter includes the skill name, description, version, author, tags, triggers, and configuration requirements.

### Use with an AI Agent

Skills are designed to work with [OpenClaw](https://github.com/nicholasgriffintn/openclaw)-compatible agents. The agent reads the `SKILL.md` to understand what the skill does, when to invoke it, and how to use it.

```bash
# Example: configure an agent with exchange skills
cp -r skills/exchanges/binance-spot-api ~/my-agent/workspace/skills/
cp -r skills/exchanges/hyperliquid ~/my-agent/workspace/skills/
cp -r skills/analytics/coingecko-price ~/my-agent/workspace/skills/

# Start your agent -- it will auto-discover the skills
my-agent start
```

## Source Attribution

All skills in this repository are sourced from the [ClawHub](https://clawhub.ai) community registry and are published under the **MIT-0** license (no attribution required). Each skill includes a `SOURCE.md` file documenting its original author and source.

We gratefully acknowledge the work of both official project teams and community contributors who created these skills.

### Official Skills

Skills from verified project teams with official GitHub repos:

| Project | Skills | Source |
|---|---|---|
| [Kraken](https://www.kraken.com/) | 50 | Official skill suite |
| [Binance](https://www.binance.com/) | 20 | [binance/binance-skills-hub](https://github.com/binance/binance-skills-hub) |
| [OKX](https://www.okx.com/) | 16 | [okx/onchainos-skills](https://github.com/okx/onchainos-skills), [okx/agent-skills](https://github.com/okx/agent-skills) |
| [Gate.io](https://www.gate.io/) | 13 | ClawHub: gate-exchange |
| [Nansen](https://www.nansen.ai/) | 10 | ClawHub: nansen-devops |
| [Uniswap](https://uniswap.org/) | 8 | Official skill suite |
| [CoinMarketCap](https://coinmarketcap.com/) | 7 | ClawHub: bryan-cmc |
| [Bitget](https://www.bitget.com/) | 7 | [BitgetLimited/agent_hub](https://github.com/BitgetLimited/agent_hub) |
| [KuCoin](https://www.kucoin.com/) | 7 | Official skill suite |
| [Lightning Labs](https://lightning.engineering/) | 3 | ClawHub: roasbeef (CTO) |
| [OpenSea](https://opensea.io/) | 2 | ClawHub: dfinzer (CEO) |
| [SushiSwap](https://www.sushi.com/) | 2 | ClawHub: 0xmasayoshi (CTO) |
| [Coinbase](https://www.coinbase.com/) | 1 | [coinbase/agentkit](https://github.com/coinbase/agentkit) |
| [Alchemy](https://www.alchemy.com/) | 1 | [alchemyplatform/alchemy-mcp-server](https://github.com/alchemyplatform/alchemy-mcp-server) |
| + more | -- | Virtuals, XMTP, ElizaOS, deBridge, GOAT, Tatum, etc. |

### Community Skills

Community-contributed skills from prolific contributors including jolestar, ivangdavila, mosonchan2023, squirt11e, and many others. Each skill's `SOURCE.md` credits the original author.

## Submit a Skill

We welcome contributions from the community. Whether you have built a new skill or discovered an MCP server that should be listed, we want to hear from you.

### How to Submit

1. **Fork** this repository
2. **Add your skill** following the [skill format](#skill-format) and guidelines in [CONTRIBUTING.md](CONTRIBUTING.md)
3. **Open a pull request** with a clear description of your submission
4. **Wait for review** -- all submissions are reviewed for security and quality before merging

### What We Are Looking For

- Skills for protocols, exchanges, or tools not yet covered
- MCP servers for crypto-related APIs and blockchains
- Improvements to existing skills (better docs, more triggers, bug fixes)
- Official skills from project teams (reach out to get the "official" badge)

### Submission Quality Standards

- Clear, accurate documentation in `SKILL.md`
- No hardcoded credentials or API keys
- Proper attribution in `SOURCE.md`
- Correct categorization and `kebab-case` naming

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full submission guide, including MCP server submission steps and security review requirements.

## Roadmap

See [ROADMAP.md](ROADMAP.md) for our development plans, including planned features like a CLI installer, search API, community rating system, and more.

## License

This project is licensed under **AGPL-3.0** -- see [LICENSE](LICENSE) for details.

Individual skills retain their original **MIT-0** license as published on ClawHub. See [THIRD_PARTY_LICENSES](THIRD_PARTY_LICENSES) for full attribution.

## Acknowledgments

- [ClawHub](https://clawhub.ai) -- The skill registry where all skills originate
- [OpenClaw](https://github.com/nicholasgriffintn/openclaw) -- The agent framework powering skills
- All original skill authors -- see `SOURCE.md` in each skill directory for individual credits
