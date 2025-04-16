import feedparser
from datetime import datetime
import re
import os

# ─── Configuration ─────────────────────────────────────────────────────────────

RSS_FEED_URL = os.getenv("RSS_FEED_URL", "https://medium.com/feed/@muppedaanvesh")
README_FILE   = "READMEBlog.md"
START_MARKER  = "<!-- BLOG-POST-LIST:START -->"
END_MARKER    = "<!-- BLOG-POST-LIST:END -->"

# List of Medium categories to include (lowercase). 
# Script will match if ANY of these appears in an entry's tags.
TARGET_CATEGORIES = ["kubernetes", "k8s"]

# ─── Fetch & Filter ────────────────────────────────────────────────────────────

def fetch_filtered_posts(feed_url, categories):
    """
    Fetches RSS feed, returns list of dicts for entries
    that have at least one category in `categories`.
    """
    feed = feedparser.parse(feed_url)
    posts = []
    for entry in feed.entries:
        entry_tags = [tag.term.lower() for tag in entry.get("tags", [])]
        if any(cat in entry_tags for cat in categories):
            # format date as YYYY‑MM‑DD
            dt = datetime(*entry.published_parsed[:6])
            posts.append({
                "title":     entry.title.strip(),
                "link":      entry.link.strip(),
                "published": dt.strftime("%Y-%m-%d")
            })
    return posts

# ─── Read & Parse README ───────────────────────────────────────────────────────

def read_readme(path):
    return open(path, "r", encoding="utf-8").read()

def write_readme(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def extract_table_and_posts(md):
    """
    Returns (before, table_lines, after, existing_links)
    where:
      - before: text up to and including START_MARKER
      - table_lines: list of markdown-table rows (excluding header)
      - after: text from END_MARKER onward
      - existing_links: set of URLs already in that table
    """
    pattern = re.compile(
        rf"(?P<before>.*?{START_MARKER}\s*\n)"
        rf"(?P<table>[\s\S]*?)"
        rf"(?P<after>\n\s*{END_MARKER}[\s\S]*)",
        re.MULTILINE
    )
    m = pattern.search(md)
    if not m:
        raise ValueError("Could not find BLOG-POST-LIST markers in README.md")
    before     = m.group("before")
    table_block = m.group("table").strip().splitlines()
    after      = m.group("after")

    # first two lines are header rows
    header = table_block[:2]
    rows   = table_block[2:]

    # collect existing links
    existing_links = set(
        re.search(r"\[.*?\]\((.*?)\)", row).group(1)
        for row in rows
        if re.search(r"\[.*?\]\((.*?)\)", row)
    )
    return before, header, rows, after, existing_links

# ─── Build Updated Table ───────────────────────────────────────────────────────

def build_final_table(header, old_rows, new_posts, existing_links):
    """
    Returns the complete table as a list of lines,
    appending only those new_posts whose link isn't in existing_links.
    """
    # filter out duplicates
    to_add = [p for p in new_posts if p["link"] not in existing_links]

    # renumber all rows: old + to_add
    final_rows = old_rows.copy()
    start_idx  = len(old_rows) + 1
    for i, post in enumerate(to_add, start_idx):
        final_rows.append(f"| {i} | {post['published']} | [{post['title']}]({post['link']}) |")

    return header + final_rows, len(to_add)

# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    md       = read_readme(README_FILE)
    posts    = fetch_filtered_posts(RSS_FEED_URL, TARGET_CATEGORIES)
    before, header, old_rows, after, existing = extract_table_and_posts(md)
    full_table, added_count = build_final_table(header, old_rows, posts, existing)

    # stitch everything back together
    new_md = before + "\n".join(full_table) + "\n" + after
    write_readme(README_FILE, new_md)

    if added_count:
        print(f"✅ Added {added_count} new post(s).")
    else:
        print("ℹ️ No new posts to add.")

if __name__ == "__main__":
    main()
