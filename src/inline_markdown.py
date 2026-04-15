import re

from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type is TextType.TEXT:
            splitted = node.text.split(delimiter)
            if len(splitted) % 2 == 0:
                raise ValueError(f"Invalid markdown: unmatched {delimiter}")
            else:
                for i in range(0, len(splitted)):
                    if splitted[i] == "":
                        continue
                    if i % 2 == 1:
                        new_nodes.append(TextNode(splitted[i], text_type))
                    else:
                        new_nodes.append(TextNode(splitted[i], TextType.TEXT))

        else:
            new_nodes.append(node)
    return new_nodes


def extract_markdown_images(text):
    mathces = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return mathces


def extract_markdown_links(text):
    mathces = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return mathces


def split_nodes_image(old_nodes):
    new_nodes = []

    for node in old_nodes:
        matches = extract_markdown_images(node.text)
        if not matches:
            new_nodes.append(node)
            continue
        text = node.text
        for i in matches:
            splitted = text.split(f"![{i[0]}]({i[1]})", 1)
            if splitted[0]:
                new_nodes.append(TextNode(splitted[0], TextType.TEXT))
            new_nodes.append(TextNode(i[0], TextType.IMAGE, i[1]))
            text = splitted[1]
        if text:
            new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes


def split_nodes_links(old_nodes):
    new_nodes = []

    for node in old_nodes:
        matches = extract_markdown_links(node.text)
        if not matches:
            new_nodes.append(node)
            continue
        text = node.text
        for i in matches:
            splitted = text.split(f"[{i[0]}]({i[1]})", 1)
            if splitted[0]:
                new_nodes.append(TextNode(splitted[0], TextType.TEXT))
            new_nodes.append(TextNode(i[0], TextType.LINK, i[1]))
            text = splitted[1]
        if text:
            new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes


def text_to_textnodes(text):
    node = TextNode(text, TextType.TEXT)
    node_bold = split_nodes_delimiter([node], "**", TextType.BOLD)
    node_italic = split_nodes_delimiter(node_bold, "_", TextType.ITALIC)
    node_code = split_nodes_delimiter(node_italic, "`", TextType.CODE)

    node_image = split_nodes_image(node_code)
    nodes = split_nodes_links(node_image)

    return nodes
