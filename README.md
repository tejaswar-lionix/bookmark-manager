# bookmark-manager

Save, search, and tag bookmarks in JSON.

## Usage

```bash
python3 -c "from bookmarks import *; b=add_bookmark([], 'Python', 'https://docs.python.org', ['docs']); print(to_markdown(b))"
python3 -c "from bookmarks import from_html; print(from_html('<a href=\"https://example.com\">Example</a>'))"
```

## Features

- Validated bookmarks with normalized tags
- Search across titles, URLs, and tags
- Markdown export with to_markdown(bookmarks)
- Netscape-style HTML import with from_html(html_text) and import_html(path)

## Tests

```bash
python3 -m unittest -q
```

## License

MIT
