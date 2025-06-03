from ast import Break
from numbers import Number
import re

from enums import TextType, BlockType
from textnode import TextNode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        if old_node.text.count(delimiter) % 2 == 1:
            raise Exception(f"Odd number ({old_node.text.count(delimiter)}) of delimiter!")
        
        split_text_nodes = old_node.text.split(delimiter)
        split_nodes = []
        for i in range(len(split_text_nodes)):
            if i % 2 == 0:
                split_nodes.append(TextNode(split_text_nodes[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(split_text_nodes[i], text_type))

        new_nodes.extend(split_nodes)

    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes(old_nodes, node_type):
    all_new_nodes = []
    for node in old_nodes:
        new_nodes = []
        extracted_links = None
        split_delimiter = ''

        if node_type == TextType.IMAGE:
            extracted_links = extract_markdown_images(node.text)
            split_delimiter = '!'

        if node_type == TextType.LINK:
            extracted_links = extract_markdown_links(node.text)

        remaining_text = node.text

        if len(extracted_links) == 0:
            all_new_nodes.append(node)
            continue
        
        for link in extracted_links:
            sections = remaining_text.split(f"{split_delimiter}[{link[0]}]({link[1]})", 1)
            remaining_text = sections[1]
            if len(sections[0]) > 0:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))

            new_nodes.append(TextNode(link[0], node_type, link[1]))

        if len(remaining_text) > 0:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))

        all_new_nodes.extend(new_nodes)

    return all_new_nodes
    
def split_nodes_image(old_nodes):
    return split_nodes(old_nodes, TextType.IMAGE)

def split_nodes_link(old_nodes):
    return split_nodes(old_nodes, TextType.LINK)

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def markdown_to_blocks(markdown):
    blocks = markdown.strip().split("\n\n")
    markdown_blocks = []
    for block in blocks:
        strip_block = block.strip()
        if strip_block != '':
            markdown_blocks.append(strip_block)

    return markdown_blocks

def block_to_block_type(block):
    block_patern = r"^#{1,6}\s\S.*"
    if bool(re.match(block_patern, block)):
        return BlockType.HEADING
    
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    
    splited_blocks = block.strip().split("\n")

    is_quote = True
    for line in splited_blocks:
        if not line.startswith(">"):
            is_quote = False
            break

    if is_quote:
        return BlockType.QUOTE
    
    is_unordered_list = True
    for line in splited_blocks:
        if not line.startswith("- "):
            is_unordered_list = False
            break

    if is_unordered_list:
        return BlockType.UNORDERED_LIST
    
    is_ordered_list = True
    ordered_list_patern = r"^[0-9]+\.\s"
    for i in range(0, len(splited_blocks)):

        regex_match = re.match(ordered_list_patern, splited_blocks[i])
        if not regex_match:
            is_ordered_list = False
            break

        index_number = f"{i + 1}. "
        list_number = regex_match.group()

        if index_number != list_number:
            is_ordered_list = False
            break

    if is_ordered_list:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH