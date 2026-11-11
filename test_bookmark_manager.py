import unittest

from bookmarks import add_bookmark, by_tag, remove, search


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

    def test_remove(self):
        bookmarks = remove(self.bookmarks, 0)
        self.assertEqual([item["title"] for item in bookmarks], ["GitHub"])


if __name__ == "__main__":
    unittest.main()
