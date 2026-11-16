#!/usr/bin/env python3
"""Save, search, and tag bookmarks in a JSON file."""
import json
import os
from html.parser import HTMLParser

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


class _BookmarkHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.bookmarks = []
        self._href = None
        self._text = []
        self._tags = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() != "a":
            return
        attributes = dict(attrs)
        self._href = attributes.get("href")
        self._text = []
        self._tags = (attributes.get("tags") or "").split(",")

    def handle_data(self, data):
        if self._href is not None:
            self._text.append(data)

    def handle_endtag(self, tag):
        if tag.lower() != "a" or self._href is None:
            return
        href = self._href
        self._href = None
        if not href or not href.startswith(("http://", "https://")):
            return
        title = "".join(self._text).strip() or href
        tags = []
        for value in self._tags:
            value = value.strip().lower()
            if value and value not in tags:
                tags.append(value)
        self.bookmarks.append({"title": title, "url": href, "tags": tags})


def from_html(html_text):
    """Extract bookmarks from anchor tags in an HTML document."""
    parser = _BookmarkHTMLParser()
    parser.feed(html_text)
    parser.close()
    return parser.bookmarks


def import_html(path):
    with open(path, encoding="utf-8") as handle:
        return from_html(handle.read())
