import unittest

from block_markdown import BlockType, block_to_block_type, markdown_to_blocks


class TestInlineNode(unittest.TestCase):
    def test_markdown_to_blocks_cases(self):
        cases = [
            # verdiğin örnek
            (
                """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
    """,
                [
                    "This is **bolded** paragraph",
                    "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                    "- This is a list\n- with items",
                ],
            ),
            # tek blok
            (
                "just one block",
                ["just one block"],
            ),
            # başta ve sonda boşluklar
            (
                "\n\nhello\n\nworld\n\n",
                ["hello", "world"],
            ),
            # satır içi newline (block bozulmamalı)
            (
                "line1\nline2\n\nline3",
                ["line1\nline2", "line3"],
            ),
        ]

        for md, expected in cases:
            with self.subTest(md=md):
                result = markdown_to_blocks(md)
                self.assertEqual(result, expected)

    # HEADING
    def test_heading_h1(self):
        self.assertEqual(block_to_block_type("# Başlık"), BlockType.HEADING)

    def test_heading_h6(self):
        self.assertEqual(block_to_block_type("###### Başlık"), BlockType.HEADING)

    def test_heading_no_space(self):
        self.assertNotEqual(block_to_block_type("#Başlık"), BlockType.HEADING)

    def test_heading_seven_hashes(self):
        self.assertNotEqual(block_to_block_type("####### Başlık"), BlockType.HEADING)

    # CODE
    def test_code_block(self):
        self.assertEqual(
            block_to_block_type("```\nprint('hello')\n```"), BlockType.CODE
        )

    def test_code_block_multiline(self):
        self.assertEqual(block_to_block_type("```\nline1\nline2\n```"), BlockType.CODE)

    def test_code_block_no_closing(self):
        self.assertNotEqual(block_to_block_type("```\nprint('hello')"), BlockType.CODE)

    # QUOTE
    def test_quote_single_line(self):
        self.assertEqual(block_to_block_type(">alıntı"), BlockType.QUOTE)

    def test_quote_multiline(self):
        self.assertEqual(block_to_block_type(">satır1\n>satır2"), BlockType.QUOTE)

    def test_quote_missing_prefix(self):
        self.assertNotEqual(block_to_block_type(">satır1\nsatır2"), BlockType.QUOTE)

    # UNORDERED LIST
    def test_unordered_list(self):
        self.assertEqual(
            block_to_block_type("- elma\n- armut"), BlockType.UNORDERED_LIST
        )

    def test_unordered_list_missing_prefix(self):
        self.assertNotEqual(
            block_to_block_type("- elma\narmut"), BlockType.UNORDERED_LIST
        )

    # ORDERED LIST
    def test_ordered_list(self):
        self.assertEqual(
            block_to_block_type("1. bir\n2. iki\n3. üç"), BlockType.ORDERED_LIST
        )

    def test_ordered_list_wrong_order(self):
        self.assertNotEqual(
            block_to_block_type("1. bir\n3. üç"), BlockType.ORDERED_LIST
        )

    def test_ordered_list_not_starting_with_one(self):
        self.assertNotEqual(
            block_to_block_type("2. iki\n3. üç"), BlockType.ORDERED_LIST
        )

    # PARAGRAPH
    def test_paragraph(self):
        self.assertEqual(block_to_block_type("düz metin"), BlockType.PARAGRAPH)
