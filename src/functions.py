import re

from enums import TextType, BlockType
from textnode import TextNode, text_node_to_html_node
from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode

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

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)

    return ParentNode("div", children)
    
def block_to_html_node(block):
    block_type = block_to_block_type(block)
    match(block_type):
        case BlockType.PARAGRAPH:
            return paragraph_to_html_node(block)
        case BlockType.HEADING:
            return heading_to_html_node(block)
        case BlockType.CODE:
            return code_to_html_node(block)
        case BlockType.ORDERED_LIST:
            return olist_to_html_node(block)
        
def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)

    return children

def olist_to_html_node(block):
    list_items = block.split("\n")
    html_items = []
    for item in list_items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)

def ulist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)

def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block[4:-3]
    raw_text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])

def heading_to_html_node(block):
    heading = block.split(" ")
    lines = " ".join(heading[1:])
    text = " ".join(lines.split("\n"))

    heading_size = len(heading[0])
    children = text_to_children(text)

    return ParentNode(f"h{heading_size}", children)