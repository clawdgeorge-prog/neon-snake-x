# MEMORY - Long-term memories about Brant and setup
Last Updated: 2026-03-10

## Today's Joke (AI-themed)
> Why do programmers always mix up Halloween and Christmas?
> Because `Oct 31 = Dec 25` 🐍

## Skills & Tools Locations
- **Earnings Prediction:** `~/.openclaw/earnings-prediction/SKILL.md`
- **Workspace Skills:** `~/.openclaw/skills/`
- **Workspace Skills (alt):** `~/.openclaw/workspace/skills/`

## About Brant
- Name: Brant
- Timezone: America/Denver
- Goal: Retire in 5 years with $5M
- Prefers casual tone, occasional humor
- Telegram: 8544038857

## Memory System
- Daily notes: memory/YYYY-MM-DD.md — raw session logs, written automatically, load on-demand
- MEMORY.md: curated long-term brain — load every heartbeat (~3K tokens)
- projects.md: compact project registry — load every heartbeat (~1K tokens)
- Vector DB: PostgreSQL + pgvector, semantic search via AI embeddings
- Smart loading: only projects.md + MEMORY.md at startup. Daily notes + vector search = on-demand only.

## Setup History

### 2026-02-24 - Initial Setup
- Telegram connected and locked to Brant's user ID
- Whisper installed for voice transcription
- Edge TTS for voice messages
- Daily backup system set up (iCloud-synced)
- Desktop shortcut to backup folder

### 2026-02-27 - Configuration
- Restored OpenClaw from backup
- Identity set: George 🦦
- Telegram locked down: allowlist only, can only send to Brant
- Created X-Trending skill (5am cron)
- Created earnings-prediction skill

### 2026-02-28 - Core Systems Built
- RAG Knowledge Base: ~/rag-kb/ with SQLite + sentence-transformers
- Sub-agents: 4 configured (coder + 3 generic)
- Self-Improvement System: tests, health checks, innovation scout
- Cron jobs expanded

### 2026-03-04 - Business Listings Launch
- Comprehensive business listings scraper for Utah & Idaho
- Target: Businesses $1M-$6M with $500K+ earnings
- Dashboard: http://localhost:8765
- 11-14 listings, 91 proactive outreach companies
- Mark Paul / CMI briefing created

### 2026-03-07 - Research Marathon
- Major research on AI trends, business opportunities
- Created 8 hourly cron jobs for continued research (12am-7am)
- Research documents:
  - PRIORITIZED-IDeas-2026-03-07.md (tiered project ideas)
  - research-findings-2026-03-07.md
  - research-business.md
  - research-tech.md
  - research-productivity.md
- Key discoveries: ai-hedge-fund (46K stars), AFFiNE, voice dictation trends

## Neon Snake X Game
- Location: `~/.openclaw/workspace/game.html`
- Full-featured snake game with neon aesthetics, power-ups, achievements, difficulty levels
- Open in browser to play anytime: `open ~/.openclaw/workspace/game.html`

## REDi Health (Researched via Grok on 2026-02-24)
Data-driven healthcare analytics company (founded 2021), Roosevelt, Utah. Specializes in rural/community hospitals.

**Key info:**
- Founded: 2021 by John Wadsworth and Jeff
- Mission: Empower small/rural hospitals to unlock data potential
- Products: Revenue Optimization, Clinical Outcomes, Operational Efficiency, Change Management Consulting

**RHTP Proposals:** Sustainability Roadmap, Outcomes-Based Reporting, Partnership with SORHs

- Full document: memory/REDi-Health-RHTP.md

## Systems & Infrastructure

### OpenClaw
- Location: ~/.openclaw/
- Running on: Mac mini
- Telegram bot: 8785538301:AAEbMHdZ-3INxV0OUnfQoSCehxD4uEXPurI

### Backup System
- Script: ~/openclaw_backup.sh
- Schedule: 3x daily (1am, 9am, 1pm)
- Backup check: 5x daily (4am, 8am, 12pm, 4pm, 8pm)
- Backup-on-wake script created
- Location: ~/Documents/OpenClawBackup

### Active Crons
- Backup: 1am, 9am, 1pm daily
- Backup Check: 4am, 8am, 12pm, 4pm, 8pm daily
- X-Trending: 5am daily
- Business listings: 6am, 12pm, 6pm daily (via LaunchAgents / scraper_with_retry.sh)
- Business email check: every 30 min (via LaunchAgent / check_email.sh)
- Business site discovery: every 30 min (via LaunchAgents / site-discovery.sh and site_discovery.sh)
- Innovation: 7am daily
- Self-improvement: 2am, 2:30am, 2:45am, 3am (varied)

### Projects
| Project | Status | Notes |
|---------|--------|-------|
| OpenClaw Agent | Live | Personal AI assistant |
| Business Listings Scraper | Live | Utah/Idaho SMB acquisitions |
| Earnings Prediction | Live | Multi-AI analysis |
| RAG Knowledge Base | Live | Local semantic search |
| Self-Improvement System | Live | Automated tests, health |
| Vector Memory | In Progress | Semantic search |
| Mark Paul/CMI Briefing | Complete | Meeting prep |

## Preferences
- Casual tone
- Always back up openclaw.json before changes
- Proactive approach - fix issues without asking
- Keep George (main session) on OpenAI when configured
- Keep routine cron jobs, scraping, and spawned agents on MiniMax by default
- Only switch subagents/workloads to OpenAI when Brant and George agree it’s needed
- Prefer one stable daily maintenance/game cron over many hourly spammy ones
- For cron jobs, do not ask the worker to send messages directly; have the worker return text and let cron delivery send it

## Key Learnings

### Browser Automation
- Sub-agents struggle with AI chat sites (Grok, ChatGPT, Gemini)
- Earnings analysis better run in main session
- ~600s timeout, 3 retries per site

### Security Notes (March 7)
- AI OSINT can build complete profiles from name in 15 min
- Voice cloning from photos now possible
- Agent security with shell access is risky

## File Locations
- OpenClaw: ~/.openclaw/
- Business Listings: ~/.openclaw/business-listings/
- RAG KB: ~/.openclaw/workspace/rag-kb/
- Self-Improvement: ~/.openclaw/self-improvement/
- Memory: ~/.openclaw/workspace/memory/

## Lessons Learned (Critical)

### Memory Persistence (March 10)
- I wake up fresh each session - no memory of previous sessions unless it's in files
- MUST check vector memory when I don't know something user asks about
- AGENTS.md updated with CRITICAL reminder to check vector DB
- Game was created but never logged - found only via file search
- Joke cron existed but delivery was broken - fixed delivery config
- Business listings automation is partly outside OpenClaw cron, using macOS LaunchAgents
- Site discovery failure root cause: `site-discovery.sh` tried to execute `main.py` directly; fixed to use `python3 ~/.openclaw/business-listings/main.py`
- **Always save important things to MEMORY.md or daily notes immediately**

## Neon Snake X Game
- Location: `~/.openclaw/workspace/game.html`
- Full-featured snake game with neon aesthetics, power-ups, achievements, difficulty levels
- Open in browser to play anytime: `open ~/.openclaw/workspace/game.html`
- Desktop shortcut created: `~/Desktop/NeonSnakeX.html`
- Backup: already included in ~/.openclaw backup
