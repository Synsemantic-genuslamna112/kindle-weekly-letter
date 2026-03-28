# Kindle Weekly Letter

Automated weekly Kindle newsletter powered by Claude Code. AI research agents collect articles daily across customizable topics, compile them into a readable EPUB book, and deliver to your Kindle every Sunday.

<p align="center">
  <img src="assets/kindle_screenshot_1.png" width="380" alt="Weekly Tech Digest cover page on Kindle" />
  &nbsp;&nbsp;
  <img src="assets/kindle_screenshot_2.png" width="380" alt="Full article reading experience on Kindle" />
</p>

<p align="center">
  <em>Cover page with all topics listed &nbsp;|&nbsp; Full articles readable directly on Kindle — no links needed</em>
</p>

## How It Works

```
Mon-Sat: 6 AI agents research topics daily, collecting 10 articles each
Sunday:  Articles compiled into EPUB → delivered to your Kindle
```

1. **Daily Collection** — Research agents use web search to find the best articles published each day. Articles accumulate in a local store, deduped by URL. Each topic pauses at 10 articles.
2. **Sunday Compilation** — All collected articles are proposed for your approval. After you approve, full article content is fetched, curated into 400-800 word readable pieces, formatted into an EPUB book, and emailed to your Kindle.

## Built-in Topics

| # | Topic | Audience |
|---|-------|----------|
| 1 | English for Software Engineers | Non-native speakers in tech |
| 2 | AI Engineering News | CTO-level engineers |
| 3 | iOS Engineering | Professional iOS developers |
| 4 | Travel App Business | App founders/product leads |
| 5 | Singapore & Korea News | English-only, official publishers |
| 6 | C++ / C / Rust / Python | Systems & scripting engineers |

Topics are fully customizable — add your own with `/add-topic`.

## Quick Start

### Prerequisites
- [Claude Code](https://claude.ai/claude-code) CLI installed
- Python 3.12+
- An email account (Gmail, Yahoo, Outlook, iCloud)
- A Kindle device with a Send-to-Kindle email address

### Setup

```bash
git clone https://github.com/ShawnBaek/kindle-weekly-letter.git
cd kindle-letter
```

Then in Claude Code:
```
/setup-kindle
```

This will walk you through:
1. Installing Python dependencies
2. Configuring your email (SMTP + app password)
3. Finding your Kindle email address
4. Sending a test EPUB
5. Setting up daily/weekly scheduling

### Manual Usage

```
/collect-now     # Run daily collector immediately
/compile-now     # Compile EPUB and send to Kindle now
```

## Slash Commands

| Command | Description |
|---------|-------------|
| `/setup-kindle` | Full setup wizard (email, Kindle, scheduling) |
| `/add-topic [name]` | Add a custom research topic |
| `/sources list` | View all sources with vote counts |
| `/sources vote [topic] [source]` | Upvote a source |
| `/sources unvote [topic] [source]` | Downvote a source |
| `/sources add [topic] [name] [url]` | Add a new source |
| `/sources remove [topic] [name]` | Deactivate a source |
| `/collect-now` | Trigger daily article collection |
| `/compile-now` | Trigger EPUB compilation and delivery |

## Customizing Sources

Each topic has a list of preferred sources in `sources.json`. Sources have vote counts that determine priority — higher voted sources are searched first.

```bash
# View sources
/sources list

# Add a source
/sources add ios "SwiftLee" "swiftlee.com"

# Vote for a source
/sources vote ai_news "Anthropic Blog"
```

Edit `sources.json` directly for bulk changes. Agents also discover new sources beyond this list each week.

## Adding Custom Topics

```
/add-topic Kubernetes
```

You'll be asked for:
- Topic name and audience
- Focus areas (3-5 subtopics)
- Preferred sources
- What to avoid

The skill creates the agent prompt, registers the topic, and updates the collectors.

## Email Providers

| Provider | SMTP Host | Port | App Password |
|----------|-----------|------|--------------|
| Gmail | smtp.gmail.com | 465 | Google Account → Security → App Passwords |
| Yahoo | smtp.mail.yahoo.com | 465 | Account Security → Generate app password |
| Outlook | smtp-mail.outlook.com | 587 | Microsoft Account → Security → App Passwords |
| iCloud | smtp.mail.me.com | 587 | appleid.apple.com → App-Specific Passwords |

## Plugin Installation

If you want to install this as a Claude Code plugin:

```
/plugin marketplace add https://raw.githubusercontent.com/ShawnBaek/kindle-weekly-letter/main/marketplace.json
/plugin install kindle-letter
```

## Project Structure

```
kindle-letter/
├── .claude/skills/          # Slash commands
├── prompts/                 # AI agent prompts
│   ├── daily_collector.md   # Daily orchestrator
│   ├── sunday_compiler.md   # Sunday EPUB compiler
│   └── agent_*.md           # Per-topic research agents
├── src/
│   ├── epub_builder.py      # EPUB generation
│   ├── email_sender.py      # SMTP email sender
│   ├── article_store.py     # Article accumulator
│   └── config.py            # Configuration
├── sources.json             # Votable source list
├── templates/               # EPUB templates
├── styles/                  # Kindle CSS
└── output/                  # Generated EPUBs (gitignored)
```

## License

MIT
