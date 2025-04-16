import feedparser
from datetime import datetime
import re

# Configuration
RSS_FEED_URL = "https://medium.com/feed/@muppedaanvesh"
README_FILE = "READMEBlog.md"
START_MARKER = "<!-- BLOG-POST-LIST:START -->"
END_MARKER = "<!-- BLOG-POST-LIST:END -->"
TARGET_CATEGORY = "kubernetes"

def fetch_kubernetes_posts(feed_url):
    feed = feedparser.parse(feed_url)
    posts = []
    for entry in feed.entries:
        categories = [tag.term.lower() for tag in entry.tags] if 'tags' in entry else []
        if TARGET_CATEGORY.lower() in categories:
            pub_date = datetime(*entry.published_parsed[:6]).strftime("%Y-%m-%d")
            posts.append({
                "title": entry.title,
                "link": entry.link,
                "date": pub_date
            })
    return posts

def read_readme(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def write_readme(file_path, content):
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

def extract_existing_posts(readme_content):
    pattern = re.compile(f"{START_MARKER}(.*?){END_MARKER}", re.DOTALL)
    match = pattern.search(readme_content)
    if not match:
        return [], readme_content

    table_content = match.group(1).strip()
    lines = table_content.splitlines()
    existing_links = set()
    for line in lines:
        match = re.search(r"\[.*?\]\((.*?)\)", line)
        if match:
            existing_links.add(match.group(1))
    return existing_links, readme_content

def generate_table(posts, existing_links):
    table_lines = ["| No. | Date | Title |", "| --- | ---- | ----- |"]
    new_posts = [post for post in posts if post["link"] not in existing_links]
    all_posts = posts  # To maintain the order
    for idx, post in enumerate(all_posts, 1):
        table_lines.append(f"| {idx} | {post['date']} | [{post['title']}]({post['link']}) |")
    return "\n".join(table_lines), new_posts

def update_readme():
    posts = fetch_kubernetes_posts(RSS_FEED_URL)
    readme_content = read_readme(README_FILE)
    existing_links, full_content = extract_existing_posts(readme_content)
    table_md, new_posts = generate_table(posts, existing_links)

    new_section = f"{START_MARKER}\n{table_md}\n{END_MARKER}"
    updated_content = re.sub(f"{START_MARKER}.*?{END_MARKER}", new_section, full_content, flags=re.DOTALL)
    write_readme(README_FILE, updated_content)

    if new_posts:
        print(f"Added {len(new_posts)} new post(s) to the README.")
    else:
        print("No new posts found.")

if __name__ == "__main__":
    update_readme()
