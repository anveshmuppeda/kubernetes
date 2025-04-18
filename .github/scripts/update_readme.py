import feedparser
import re
import os
from datetime import datetime

# ─── Configuration ─────────────────────────────────────────────────────────────

# Medium RSS feed URL can be overridden via env var:
RSS_FEED_URL  = os.getenv("RSS_FEED_URL",
                  "https://medium.com/feed/@muppedaanvesh")  # :contentReference[oaicite:2]{index=2}
README_FILE   = "README.md"
START_MARKER  = "<!-- BLOG-POST-LIST:START -->"
END_MARKER    = "<!-- BLOG-POST-LIST:END -->"

# List of categories (lowercase) to include:
TARGET_CATEGORIES = ["kubernetes", "k8s"]

# ─── Fetch & Filter ────────────────────────────────────────────────────────────

def fetch_filtered_posts(feed_url, categories):
    """
    Parse the RSS feed and return only entries whose tags
    include at least one of `categories`.
    """
    feed  = feedparser.parse(feed_url)  # :contentReference[oaicite:3]{index=3}
    posts = []
    for entry in feed.entries:
        tags = [t.term.lower() for t in entry.get("tags", [])]
        if any(cat in tags for cat in categories):
            dt = datetime(*entry.published_parsed[:6])
            posts.append({
                "title":     entry.title.strip(),
                "link":      entry.link.strip(),
                "published": dt.strftime("%Y-%m-%d")  # ISO format :contentReference[oaicite:4]{index=4}
            })
    return posts

# ─── Read & Write README ───────────────────────────────────────────────────────

def read_readme(path):
    return open(path, "r", encoding="utf-8").read()

def write_readme(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

# ─── Extract Existing Table & Links ────────────────────────────────────────────

def extract_table_and_posts(md):
    """
    Splits `md` into:
      before: everything up to and including START_MARKER
      header: first two lines of the table
      rows:   existing table rows
      after:  everything from END_MARKER onward
      existing_links: set of URLs already in `rows`
    """
    pattern = re.compile(
        rf"(?P<before>[\s\S]*?{START_MARKER}\s*\n)"
        rf"(?P<table>[\s\S]*?)"
        rf"(?P<after>\n\s*{END_MARKER}[\s\S]*)"
    )  # [\s\S] trick matches ALL chars, including newlines :contentReference[oaicite:5]{index=5}

    m = pattern.search(md)
    if not m:
        raise ValueError("Could not find BLOG-POST-LIST markers in README.md")

    before      = m.group("before")
    table_lines = m.group("table").strip().splitlines()
    after       = m.group("after")

    header = table_lines[:2]
    rows   = table_lines[2:]

    existing_links = {
        re.search(r"\[.*?\]\((.*?)\)", row).group(1)
        for row in rows
        if re.search(r"\[.*?\]\((.*?)\)", row)
    }
    return before, header, rows, after, existing_links

# ─── Build Final Table ─────────────────────────────────────────────────────────

def build_final_table(header, old_rows, new_posts, existing_links):
    """
    Returns the full table lines (header + old_rows + appended new rows),
    plus the count of how many new rows were added.
    """
    to_add = [p for p in new_posts if p["link"] not in existing_links]
    final = old_rows.copy()
    start = len(old_rows) + 1

    for i, post in enumerate(to_add, start):
        final.append(f"| {i} | {post['published']} | [{post['title']}]({post['link']}) |")

    return header + final, len(to_add)

# ─── Main Execution ────────────────────────────────────────────────────────────

def main():
    md         = read_readme(README_FILE)
    posts      = fetch_filtered_posts(RSS_FEED_URL, TARGET_CATEGORIES)
    before, header, rows, after, existing = extract_table_and_posts(md)
    full_table, added_count = build_final_table(header, rows, posts, existing)

    new_md = before + "\n".join(full_table) + "\n" + after
    write_readme(README_FILE, new_md)

    if added_count:
        print(f"✅ Added {added_count} new post(s).")
    else:
        print("ℹ️ No new posts to add.")

if __name__ == "__main__":
    main()
