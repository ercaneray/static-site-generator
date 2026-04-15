import unittest

from inline_markdown import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_links,
    text_to_textnodes,
)
from textnode import TextNode, TextType


class TestInlineNode(unittest.TestCase):
    def run_cases(self, cases, delimiter, text_type):
        for input_text, expected in cases:
            with self.subTest(input=input_text):
                node = TextNode(input_text, TextType.TEXT)
                result = split_nodes_delimiter([node], delimiter, text_type)
                simplified = [(n.text, n.text_type) for n in result]
                self.assertEqual(simplified, expected)

    def test_bold(self):
        bold_cases = [
            ("**a**", [("a", TextType.BOLD)]),
            (
                "a **b** c",
                [("a ", TextType.TEXT), ("b", TextType.BOLD), (" c", TextType.TEXT)],
            ),
            (
                "**a** **b**",
                [
                    ("a", TextType.BOLD),
                    (" ", TextType.TEXT),
                    ("b", TextType.BOLD),
                ],
            ),
        ]
        self.run_cases(bold_cases, "**", TextType.BOLD)

    def test_italic(self):
        italic_cases = [
            ("*a*", [("a", TextType.ITALIC)]),
            (
                "a *b* c",
                [("a ", TextType.TEXT), ("b", TextType.ITALIC), (" c", TextType.TEXT)],
            ),
            (
                "*a* *b*",
                [
                    ("a", TextType.ITALIC),
                    (" ", TextType.TEXT),
                    ("b", TextType.ITALIC),
                ],
            ),
        ]
        self.run_cases(italic_cases, "*", TextType.ITALIC)

    def test_code(self):
        code_cases = [
            ("`a`", [("a", TextType.CODE)]),
            (
                "a `b` c",
                [("a ", TextType.TEXT), ("b", TextType.CODE), (" c", TextType.TEXT)],
            ),
            (
                "`a` `b`",
                [
                    ("a", TextType.CODE),
                    (" ", TextType.TEXT),
                    ("b", TextType.CODE),
                ],
            ),
        ]
        self.run_cases(code_cases, "`", TextType.CODE)

    def test_invalid(self):
        invalid_cases = [
            ("**a", "**"),
            ("a**", "**"),
            ("*a", "*"),
            ("a*", "*"),
            ("`a", "`"),
            ("a`", "`"),
        ]

        for text, delimiter in invalid_cases:
            with self.subTest(input=text):
                node = TextNode(text, TextType.TEXT)
                with self.assertRaises(ValueError):
                    split_nodes_delimiter([node], delimiter, TextType.BOLD)

    def test_extract_markdown_images_basic(self):
        cases = [
            (
                "![image](https://i.imgur.com/zjjcJKZ.png)",
                [("image", "https://i.imgur.com/zjjcJKZ.png")],
            ),
            (
                "Text ![img1](url1) more text",
                [("img1", "url1")],
            ),
            (
                "! !",
                [],
            ),
        ]

        for text, expected in cases:
            with self.subTest(text=text):
                result = extract_markdown_images(text)
                self.assertListEqual(result, expected)

    def test_extract_markdown_images_edge_cases(self):
        cases = [
            ("", []),
            ("no images here", []),
            ("![](url)", [("", "url")]),  # boş alt text
            ("![alt]()", [("alt", "")]),  # boş url
        ]

        for text, expected in cases:
            with self.subTest(text=text):
                result = extract_markdown_images(text)
                self.assertListEqual(result, expected)

    def test_extract_markdown_links_basic(self):
        cases = [
            ("[google](https://google.com)", [("google", "https://google.com")]),
            ("text [link](url) more", [("link", "url")]),
            (" ", []),
        ]

        for text, expected in cases:
            with self.subTest(text=text):
                result = extract_markdown_links(text)
                self.assertEqual(result, expected)

    def test_extract_markdown_links_edge(self):
        cases = [
            ("", []),
            ("no links here", []),
            ("[](url)", [("", "url")]),  # boş text
            ("[text]()", [("text", "")]),  # boş url
        ]

        for text, expected in cases:
            with self.subTest(text=text):
                result = extract_markdown_links(text)
                self.assertEqual(result, expected)

    def test_split_images_cases(self):
        cases = [
            # basic
            (
                "Hello ![alt](url) world",
                [
                    TextNode("Hello ", TextType.TEXT),
                    TextNode("alt", TextType.IMAGE, "url"),
                    TextNode(" world", TextType.TEXT),
                ],
            ),
            # başta
            (
                "![alt](url) hello",
                [
                    TextNode("alt", TextType.IMAGE, "url"),
                    TextNode(" hello", TextType.TEXT),
                ],
            ),
            # sonda
            (
                "hello ![alt](url)",
                [
                    TextNode("hello ", TextType.TEXT),
                    TextNode("alt", TextType.IMAGE, "url"),
                ],
            ),
            # sadece image
            (
                "![alt](url)",
                [
                    TextNode("alt", TextType.IMAGE, "url"),
                ],
            ),
            # hiç image yok
            (
                "just plain text",
                [
                    TextNode("just plain text", TextType.TEXT),
                ],
            ),
        ]

        for text, expected in cases:
            with self.subTest(text=text):
                node = TextNode(text, TextType.TEXT)
                result = split_nodes_image([node])
                self.assertEqual(result, expected)

    def test_split_links_cases(self):
        cases = [
            (
                "Hello [alt](url) world",
                [
                    TextNode("Hello ", TextType.TEXT),
                    TextNode("alt", TextType.LINK, "url"),
                    TextNode(" world", TextType.TEXT),
                ],
            ),
            (
                "[alt](url) hello",
                [
                    TextNode("alt", TextType.LINK, "url"),
                    TextNode(" hello", TextType.TEXT),
                ],
            ),
            (
                "hello [alt](url)",
                [
                    TextNode("hello ", TextType.TEXT),
                    TextNode("alt", TextType.LINK, "url"),
                ],
            ),
            (
                "[alt](url)",
                [
                    TextNode("alt", TextType.LINK, "url"),
                ],
            ),
            (
                "no links here",
                [
                    TextNode("no links here", TextType.TEXT),
                ],
            ),
        ]

        for text, expected in cases:
            with self.subTest(text=text):
                node = TextNode(text, TextType.TEXT)
                result = split_nodes_links([node])
                self.assertEqual(result, expected)

    def test_text_to_textnodes_cases(self):
        cases = [
            # plain text
            (
                "just text",
                [
                    TextNode("just text", TextType.TEXT),
                ],
            ),
            # bold
            (
                "this is **bold** text",
                [
                    TextNode("this is ", TextType.TEXT),
                    TextNode("bold", TextType.BOLD),
                    TextNode(" text", TextType.TEXT),
                ],
            ),
            # italic (_ ile)
            (
                "this is _italic_ text",
                [
                    TextNode("this is ", TextType.TEXT),
                    TextNode("italic", TextType.ITALIC),
                    TextNode(" text", TextType.TEXT),
                ],
            ),
            # code
            (
                "this is `code` text",
                [
                    TextNode("this is ", TextType.TEXT),
                    TextNode("code", TextType.CODE),
                    TextNode(" text", TextType.TEXT),
                ],
            ),
            # link
            (
                "go to [google](https://google.com)",
                [
                    TextNode("go to ", TextType.TEXT),
                    TextNode("google", TextType.LINK, "https://google.com"),
                ],
            ),
            # image
            (
                "look ![alt](img.png)",
                [
                    TextNode("look ", TextType.TEXT),
                    TextNode("alt", TextType.IMAGE, "img.png"),
                ],
            ),
            # mixed (ama nested yok)
            (
                "this is **bold** and _italic_ and `code`",
                [
                    TextNode("this is ", TextType.TEXT),
                    TextNode("bold", TextType.BOLD),
                    TextNode(" and ", TextType.TEXT),
                    TextNode("italic", TextType.ITALIC),
                    TextNode(" and ", TextType.TEXT),
                    TextNode("code", TextType.CODE),
                ],
            ),
            # link + image
            (
                "text [link](url) and ![img](src)",
                [
                    TextNode("text ", TextType.TEXT),
                    TextNode("link", TextType.LINK, "url"),
                    TextNode(" and ", TextType.TEXT),
                    TextNode("img", TextType.IMAGE, "src"),
                ],
            ),
            # back-to-back bold
            (
                "**a****b**",
                [
                    TextNode("a", TextType.BOLD),
                    TextNode("b", TextType.BOLD),
                ],
            ),
            # back-to-back italic
            (
                "_a__b_",
                [
                    TextNode("a", TextType.ITALIC),
                    TextNode("b", TextType.ITALIC),
                ],
            ),
            # sadece delimiter içeriği
            (
                "**bold**",
                [
                    TextNode("bold", TextType.BOLD),
                ],
            ),
            # hiç markdown yok
            (
                "no markdown here",
                [
                    TextNode("no markdown here", TextType.TEXT),
                ],
            ),
        ]

        for text, expected in cases:
            with self.subTest(text=text):
                result = text_to_textnodes(text)
                self.assertEqual(result, expected)
