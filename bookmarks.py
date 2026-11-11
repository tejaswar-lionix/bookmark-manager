#!/usr/bin/env python3
"""Save, search, and tag bookmarks in a JSON file."""
import json
import os

DEFAULT_PATH = os.path.expanduser("~/.bookmarks.json")


def load(path=DEFAULT_PATH):
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def save(bookmarks, path=DEFAULT_PATH):
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(bookmarks, handle, indent=2)


def add_bookmark(bookmarks, title, url, tags=None):
    if not title.strip():
        raise ValueError("title must not be empty")
    if not url.startswith(("http://", "https://")):
        raise ValueError("url must start with http:// or https://")
    clean_tags = []
    for tag in tags or []:
        tag = tag.strip().lower()
        if tag and tag not in clean_tags:
            clean_tags.append(tag)
    bookmarks.append({"title": title.strip(), "url": url, "tags": clean_tags})
    return bookmarks


def search(bookmarks, query):
    needle = query.lower()
    return [
        bookmark
        for bookmark in bookmarks
        if needle in bookmark["title"].lower()
        or needle in bookmark["url"].lower()
        or any(needle in tag for tag in bookmark["tags"])
    ]


def by_tag(bookmarks, tag):
    tag = tag.lower()
    return [bookmark for bookmark in bookmarks if tag in bookmark["tags"]]


def remove(bookmarks, index):
    return bookmarks[:index] + bookmarks[index + 1:]


def to_markdown(bookmarks):
    """Render bookmarks as a markdown list with tags."""
    lines = ["# Bookmarks", ""]
    for bookmark in bookmarks:
        tags = " ".join("#" + tag for tag in bookmark["tags"])
        suffix = " " + tags if tags else ""
        lines.append("- [%s](%s)%s" % (bookmark["title"], bookmark["url"], suffix))
    return "\n".join(lines) + "\n"
