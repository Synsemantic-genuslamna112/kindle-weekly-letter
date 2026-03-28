# Sunday EPUB Compiler

You compile the week's collected articles into an EPUB and send it to Kindle. The project is at `/Users/sungwookbaek/Dropbox/Projects/kindle-letter`.

## Step 1: Check Collection Status

```bash
source .venv/bin/activate && python3 -c "from src.article_store import get_status_summary; print(get_status_summary())"
```

Also load all articles to see what we have:
```bash
source .venv/bin/activate && python3 -c "
from src.article_store import load_articles
from src.config import TOPICS
for t in TOPICS:
    articles = load_articles(t['id'])
    print(f\"\\n{t['name']} ({len(articles)} articles):\")
    for a in articles:
        print(f\"  - {a['title']} [{a['source']}] (Confidence: {a.get('confidence', 'N/A')})\")
"
```

## Step 2: Present Proposals

Show the user ALL collected articles organized by topic:

```
══════════════════════════════════════════════════
  KINDLE WEEKLY LETTER — Week of [DATE]
  Collected Articles for Your Approval
══════════════════════════════════════════════════

📖 TOPIC 1: English for Software Engineers ([N] articles)
   1. [title] — [source] (Confidence: [high/medium/low])
      [summary]
   ...

🤖 TOPIC 2: AI Engineering News ([N] articles)
   ...

📱 TOPIC 3: iOS Engineering ([N] articles)
   ...

✈️ TOPIC 4: Travel App Business ([N] articles)
   ...

🗞️ TOPIC 5: Singapore & Korea News ([N] articles)
   ...

⚙️ TOPIC 6: C++ / C / Rust / Python ([N] articles)
   ...

══════════════════════════════════════════════════
Type 'approve' to proceed with all articles,
or specify which to keep/remove (e.g., "remove Topic 2 #3, #5")
══════════════════════════════════════════════════
```

Wait for user approval.

## Step 3: Curate FULL Content

**CRITICAL: The EPUB must be a self-contained book. The reader should NEVER need to click a link to read the full article. Every article must be fully readable within the EPUB itself. Links are for source attribution only.**

For each approved article:
1. Use `WebFetch` to retrieve the FULL content from the article URL
2. Curate it into a complete, standalone article — NOT a summary:
   - Include all key points, examples, code snippets, and explanations
   - Restructure for readability but preserve the substance
   - Add context for the target audience where helpful
   - Keep the original author's voice and insights
   - **Target 400-800 words per article** (longer is fine for rich content)
   - If the source is a tutorial or guide, include the step-by-step instructions
   - If the source has code examples, include them
3. Format as clean HTML (paragraphs, bold for key points, blockquotes for notable quotes, code blocks for code)

## Step 4: Write Content JSON

Write to `output/content.json`:
```json
{
  "title": "Weekly Tech Digest — [Month Day, Year]",
  "date": "YYYY-MM-DD",
  "sections": [
    {
      "topic": "Topic Name",
      "intro": "A compelling 2-sentence intro for this section",
      "articles": [
        {
          "title": "Article title",
          "source": "Source name",
          "url": "https://...",
          "content_html": "<p>Curated HTML content...</p>"
        }
      ]
    }
  ]
}
```

## Step 5: Build EPUB

```bash
source .venv/bin/activate && python3 -m src.epub_builder --input output/content.json --output "output/kindle_letter_$(date +%Y_%m_%d).epub"
```

## Step 6: Send to Kindle

```bash
source .venv/bin/activate && python3 -m src.email_sender --epub "output/kindle_letter_$(date +%Y_%m_%d).epub"
```

## Step 7: Save Sent History & Clear Weekly Store

After successful send, save all sent article URLs to history (prevents duplicates in future weeks), then clear the weekly store:
```bash
source .venv/bin/activate && python3 -c "
from src.article_store import load_articles, save_to_sent_history, clear_weekly
from src.config import TOPICS
all_articles = []
for t in TOPICS:
    all_articles.extend(load_articles(t['id']))
save_to_sent_history(all_articles)
print(f'Saved {len(all_articles)} URLs to sent history')
clear_weekly()
print('Weekly store cleared for next week')
"
```

## Step 8: Report

Tell the user:
- Total articles included per topic
- EPUB file location
- Whether email was sent successfully
- Any issues encountered

## Error Handling
- If a topic has 0 articles: skip it, note in report
- If WebFetch fails for an article: use the stored summary instead of full curated content
- If EPUB build fails: fix content JSON and retry
- If email fails: save EPUB, tell user to send manually
- Always produce whatever content is available
