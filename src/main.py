from leafnode import LeafNode
from parentnode import ParentNode
from textnode import TextNode, TextType, text_node_to_html_node
from functions import split_nodes_delimiter
# from htmlnode import HTMLNode

def main():
    # test_text_node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev").text_node_to_html_node()
    # test_text_node = TextNode("This is some text", TextType.BOLD)

    # test_html_node = HTMLNode("p", "Some text", {"a": "test"}, {"href": "www.none.com"})
    # test_leaf_node = LeafNode("p", "This is a paragraph of text.").to_html()
    # test_leaf_node2= LeafNode("a", "Click me!", {"href": "https://www.google.com"}).to_html()

    # print(test_leaf_node)
    # print(test_leaf_node2)

    # node = ParentNode(
    # "p",
    # [
    #     LeafNode("b", "Bold text"),
    #     LeafNode(None, "Normal text"),
    #     LeafNode("i", "italic text"),
    #     LeafNode(None, "Normal text"),
    # ])

    # node.to_html()

    # print("MAIN", text_node_to_html_node(test_text_node))


    # node = TextNode("This is text with a `code block` word", TextType.TEXT)
    node = TextNode("This is **bold text** with another **bold text**!", TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
    print("new_nodes:", new_nodes)



main()