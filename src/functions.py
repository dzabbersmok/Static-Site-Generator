import re

from textnode import TextType, TextNode

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
    