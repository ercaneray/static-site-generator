from block_markdown import BlockType, block_to_block_type, markdown_to_blocks
from htmlnode import ParentNode
from inline_markdown import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_nodes = []
    for i in blocks:
        html_nodes.append(block_to_html(i))
    div_node = ParentNode("div", html_nodes)
    return div_node


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    child_nodes = list(map(lambda x: text_node_to_html_node(x), text_nodes))
    return child_nodes


def clean_markdown_block(block):
    type = block_to_block_type(block)
    match type:
        case BlockType.PARAGRAPH:
            lines = block.splitlines()
            new_lines = list(map(lambda x: x.strip(), lines))
            return " ".join(new_lines)
        case BlockType.HEADING:
            stripped_hashes = block.lstrip("#")
            level = len(block) - len(stripped_hashes)
            text = stripped_hashes.strip()
            return (text, level)
        case BlockType.CODE:
            return block[4:-3]
        case BlockType.QUOTE:
            lines = block.splitlines()
            new_lines = list(map(lambda x: x.lstrip("> "), lines))
            return " ".join(new_lines)
        case BlockType.UNORDERED_LIST:
            lines = block.splitlines()
            new_lines = list(map(lambda x: x[2:], lines))
            return new_lines
        case BlockType.ORDERED_LIST:
            lines = block.splitlines()
            new_lines = []
            for line in lines:
                while line[0] != ".":
                    line = line[1:]
                new_lines.append(line[2:])
            return new_lines


def block_to_html(block):
    type = block_to_block_type(block)
    match type:
        case BlockType.PARAGRAPH:
            text = clean_markdown_block(block)
            children = text_to_children(text)
            parent_node = ParentNode("p", children)
            return parent_node
        case BlockType.HEADING:
            text, level = clean_markdown_block(block)
            children = text_to_children(text)
            parent_node = ParentNode(f"h{level}", children)
            return parent_node
        case BlockType.CODE:
            text = clean_markdown_block(block)
            text_node = TextNode(text, TextType.TEXT)
            code_block = ParentNode("code", [text_node_to_html_node(text_node)])
            parent_node = ParentNode(
                "pre",
                [code_block],
            )
            return parent_node
        case BlockType.QUOTE:
            text = clean_markdown_block(block)
            children = text_to_children(text)
            parent_node = ParentNode("blockquote", children)
            return parent_node
        case BlockType.UNORDERED_LIST:
            lines = clean_markdown_block(block)
            children_list = []
            for line in lines:
                children = text_to_children(line)
                node = ParentNode("li", children)
                children_list.append(node)
            parent_node = ParentNode("ul", children_list)
            return parent_node
        case BlockType.ORDERED_LIST:
            lines = clean_markdown_block(block)
            children_list = []
            for line in lines:
                children = text_to_children(line)
                node = ParentNode("li", children)
                children_list.append(node)
            parent_node = ParentNode("ol", children_list)
            return parent_node
