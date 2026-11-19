import os
import tempfile
import unittest

from bookmarks import add_bookmark, all_tags, by_tag, dedupe, remove, remove_by_tag, search

NETSCAPE_HTML = """<!DOCTYPE NETSCAPE-Bookmark-file-1>
<DL><p>
    <DT><A HREF="https://docs.python.org" TAGS="Python, Docs">Python Docs</A>
    <DT><A HREF="https://github.com" TAGS="Git, git">GitHub</A>
    <DT><A HREF="ftp://example.com">FTP</A>
</DL><p>
"""


class BookmarkTests(unittest.TestCase):
    def setUp(self):
        self.bookmarks = []
        add_bookmark(
            self.bookmarks,
            "Python docs",
            "https://docs.python.org",
            ["python", "docs", "Python"],
        )
        add_bookmark(
            self.bookmarks,
            "GitHub",
            "https://github.com",
            ["git"],
        )

    def test_add_normalises_tags(self):
        self.assertEqual(self.bookmarks[0]["tags"], ["python", "docs"])

    def test_add_rejects_bad_url(self):
        with self.assertRaises(ValueError):
            add_bookmark([], "Bad", "example.com")

    def test_search_matches_title_url_and_tags(self):
        self.assertEqual(len(search(self.bookmarks, "github")), 1)
        self.assertEqual(len(search(self.bookmarks, "python")), 1)
        self.assertEqual(len(search(self.bookmarks, "example")), 0)

    def test_by_tag(self):
        self.assertEqual([item["title"] for item in by_tag(self.bookmarks, "git")], ["GitHub"])

    def test_all_tags_unique_and_sorted(self):
        self.assertEqual(all_tags(self.bookmarks), ["docs", "git", "python"])

    def test_all_tags_empty(self):
        self.assertEqual(all_tags([]), [])

    def test_remove(self):
        bookmarks = remove(self.bookmarks, 0)
        self.assertEqual([item["title"] for item in bookmarks], ["GitHub"])

    def test_remove_by_tag_removes_matching(self):
        bookmarks = remove_by_tag(self.bookmarks, "docs")
        self.assertEqual([item["title"] for item in bookmarks], ["GitHub"])

    def test_remove_by_tag_is_case_insensitive(self):
        bookmarks = remove_by_tag(self.bookmarks, "PYTHON")
        self.assertEqual([item["title"] for item in bookmarks], ["GitHub"])

    def test_remove_by_tag_keeps_others(self):
        bookmarks = remove_by_tag(self.bookmarks, "git")
        self.assertEqual([item["title"] for item in bookmarks], ["Python docs"])

    def test_remove_by_tag_unknown_keeps_all(self):
        bookmarks = remove_by_tag(self.bookmarks, "missing")
        self.assertEqual(bookmarks, self.bookmarks)

    def test_remove_by_tag_does_not_mutate_input(self):
        original = [dict(item, tags=list(item["tags"])) for item in self.bookmarks]
        remove_by_tag(self.bookmarks, "docs")
        self.assertEqual(self.bookmarks, original)


class DedupeTests(unittest.TestCase):
    def test_merges_duplicate_urls_and_tags(self):
        bookmarks = [
            {"title": "Python", "url": "https://python.org", "tags": ["docs"]},
            {"title": "Other", "url": "https://example.com", "tags": ["misc"]},
            {"title": "Python again", "url": "https://python.org", "tags": ["docs", "lang"]},
        ]
        result = dedupe(bookmarks)
        self.assertEqual([item["url"] for item in result], [
            "https://python.org",
            "https://example.com",
        ])
        self.assertEqual(result[0]["title"], "Python")
        self.assertEqual(result[0]["tags"], ["docs", "lang"])

    def test_keeps_distinct_urls(self):
        bookmarks = [
            {"title": "A", "url": "https://a.example", "tags": []},
            {"title": "B", "url": "https://b.example", "tags": []},
        ]
        self.assertEqual(dedupe(bookmarks), bookmarks)

    def test_input_is_not_mutated(self):
        bookmarks = [
            {"title": "Python", "url": "https://python.org", "tags": ["docs"]},
            {"title": "Python again", "url": "https://python.org", "tags": ["lang"]},
        ]
        original = [dict(item, tags=list(item["tags"])) for item in bookmarks]
        dedupe(bookmarks)
        self.assertEqual(bookmarks, original)


class MarkdownTests(unittest.TestCase):
    def test_to_markdown_renders_links_and_tags(self):
        from bookmarks import to_markdown

        bookmarks = add_bookmark(
            [],
            "Python docs",
            "https://docs.python.org",
            ["python", "docs"],
        )
        markdown = to_markdown(bookmarks)
        self.assertIn("[Python docs](https://docs.python.org)", markdown)
        self.assertIn("#python #docs", markdown)


class HtmlImportTests(unittest.TestCase):
    def test_from_html_extracts_titles_urls_and_tags(self):
        from bookmarks import from_html

        bookmarks = from_html(NETSCAPE_HTML)
        self.assertEqual(
            bookmarks,
            [
                {
                    "title": "Python Docs",
                    "url": "https://docs.python.org",
                    "tags": ["python", "docs"],
                },
                {"title": "GitHub", "url": "https://github.com", "tags": ["git"]},
            ],
        )

    def test_blank_anchor_text_falls_back_to_url(self):
        from bookmarks import from_html

        bookmarks = from_html('<A HREF="https://example.com"></A>')
        self.assertEqual(bookmarks[0]["title"], "https://example.com")

    def test_non_http_links_are_skipped(self):
        from bookmarks import from_html

        bookmarks = from_html(
            '<A HREF="ftp://example.com">FTP</A>'
            '<A HREF="https://example.com">Example</A>'
        )
        self.assertEqual([item["url"] for item in bookmarks], ["https://example.com"])

    def test_tags_are_deduped(self):
        from bookmarks import from_html

        bookmarks = from_html(
            '<A HREF="https://example.com" TAGS="Python, Docs, python, DOCS">Example</A>'
        )
        self.assertEqual(bookmarks[0]["tags"], ["python", "docs"])

    def test_import_html_reads_file(self):
        from bookmarks import import_html

        with tempfile.TemporaryDirectory() as directory:
            path = os.path.join(directory, "bookmarks.html")
            with open(path, "w", encoding="utf-8") as handle:
                handle.write(NETSCAPE_HTML)
            bookmarks = import_html(path)
        self.assertEqual([item["url"] for item in bookmarks], [
            "https://docs.python.org",
            "https://github.com",
        ])


class RenameTagTests(unittest.TestCase):
    def test_renames_tag_across_bookmarks(self):
        from bookmarks import rename_tag

        bookmarks = [
            {"title": "A", "url": "https://a.com", "tags": ["docs"]},
            {"title": "B", "url": "https://b.com", "tags": ["docs", "python"]},
        ]
        rename_tag(bookmarks, "docs", "reference")
        self.assertEqual(bookmarks[0]["tags"], ["reference"])
        self.assertEqual(bookmarks[1]["tags"], ["reference", "python"])

    def test_merges_duplicate_tags(self):
        from bookmarks import rename_tag

        bookmarks = [{"title": "A", "url": "https://a.com", "tags": ["old", "new"]}]
        rename_tag(bookmarks, "old", "new")
        self.assertEqual(bookmarks[0]["tags"], ["new"])

    def test_rejects_empty_new_tag(self):
        from bookmarks import rename_tag

        with self.assertRaises(ValueError):
            rename_tag([], "old", "  ")


if __name__ == "__main__":
    unittest.main()
