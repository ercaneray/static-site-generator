import unittest

from markdown_to_html import extract_title, markdown_to_html_node


class TestMarkdownToHtml(unittest.TestCase):
    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_basic_heading(self):
        md = "# Başlık"
        self.assertEqual(extract_title(md), "Başlık")

    def test_heading_with_leading_spaces(self):
        md = "   # Başlık"
        self.assertEqual(extract_title(md), "Başlık")

    def test_multiple_lines(self):
        md = "text\n# Başlık\nmore text"
        self.assertEqual(extract_title(md), "Başlık")

    def test_ignore_non_h1(self):
        md = "## Alt başlık"
        with self.assertRaises(Exception):
            extract_title(md)

    def test_no_heading(self):
        md = "sadece text var"
        with self.assertRaises(Exception):
            extract_title(md)

    def test_missing_space(self):
        md = "#Başlık"
        with self.assertRaises(Exception):
            extract_title(md)
