import re
from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(block):

    if re.findall(r"^#{1,6} .*?", block, re.MULTILINE):
        return BlockType.HEADING
    if re.findall(r"^`{3}\n.*?`{3}$", block, re.DOTALL):
        return BlockType.CODE
    lines = block.splitlines()
    if all(re.match(r">", line) for line in lines):
        return BlockType.QUOTE
    if all(re.match(r"- ", line) for line in lines):
        return BlockType.UNORDERED_LIST
    if re.match(r"1\. ", lines[0]):
        order = 1
        for line in lines:
            if re.match(rf"{order}\. ", line):
                order += 1
                continue
            else:
                return BlockType.PARAGRAPH
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH


def markdown_to_blocks(markdown):
    splitted = markdown.split("\n\n")
    stripped = map(lambda x: x.strip(), splitted)
    result = []
    for i in list(stripped):
        if i != "":
            result.append(i)
    return result
