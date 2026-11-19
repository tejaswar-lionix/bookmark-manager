# bookmark-manager

Save, search, and tag bookmarks in JSON.

## Usage

```bash
python3 -c "from bookmarks import *; b=add_bookmark([], 'Python', 'https://docs.python.org', ['docs']); print(to_markdown(b))"
python3 -c "from bookmarks import dedupe; print(dedupe([{'title': 'Python', 'url': 'https://python.org', 'tags': ['docs']}, {'title': 'Python', 'url': 'https://python.org', 'tags': ['lang']}]))"
python3 -c "from bookmarks import from_html; print(from_html('<a href=\"https://example.com\">Example</a>'))"
python3 -c "from bookmarks import all_tags; print(all_tags([{'title': 'Python', 'url': 'https://python.org', 'tags': ['docs', 'lang']}]))"
python3 -c "from bookmarks import remove_by_tag; print(remove_by_tag([{'title': 'Python', 'url': 'https://python.org', 'tags': ['docs']}], 'docs'))"
```

## Features

- Validated bookmarks with normalized tags
- Search across titles, URLs, and tags
- List unique tags with all_tags(bookmarks)
- Remove bookmarks by tag with remove_by_tag(bookmarks, tag)
- Merge duplicate URLs with dedupe(bookmarks)
- Markdown export with to_markdown(bookmarks)
- Netscape-style HTML import with from_html(html_text) and import_html(path)

## Tests

```bash
python3 -m unittest -q
```

## Additional API

- `rename_tag(bookmarks, old, new)` renames a tag across all bookmarks and merges duplicates.

## License

MIT
