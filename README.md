# bookmark-manager

Save, search, and tag bookmarks in JSON.

## Usage

```bash
python3 -c "from bookmarks import *; b=add_bookmark([], 'Python', 'https://docs.python.org', ['docs']); print(to_markdown(b))"
```

## Features

- Validated bookmarks with normalized tags
- Search across titles, URLs, and tags
- Markdown export with to_markdown(bookmarks)

## Tests

```bash
python3 -m unittest -q
```

## License

MIT
