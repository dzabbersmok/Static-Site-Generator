from leafnode import LeafNode
from parentnode import ParentNode
from textnode import TextNode, TextType, text_node_to_html_node
from functions import split_nodes_delimiter, extract_markdown_images, split_nodes_link, text_to_textnodes
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
    # node = TextNode("This is **bold text** with another **bold text**!", TextType.TEXT)
    # new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
    # print("new_nodes:", new_nodes)

    # text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
    # print(extract_markdown_images(text))
    # print([("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])

    # node = TextNode(
    #     "No image here! Just some text...",
    #     TextType.TEXT,
    # )
    # new_nodes = split_nodes_link([node])
    # print(new_nodes)

    some_text = "This is **bold_text** with an _italic_words_ and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
    print(text_to_textnodes(some_text))

main()