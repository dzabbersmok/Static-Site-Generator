from leafnode import LeafNode
# from textnode import TextNode, TextType
# from htmlnode import HTMLNode

def main():
    # test_text_node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    # test_html_node = HTMLNode("p", "Some text", {"a": "test"}, {"href": "www.none.com"})
    test_leaf_node = LeafNode("p", "This is a paragraph of text.").to_html()
    test_leaf_node2= LeafNode("a", "Click me!", {"href": "https://www.google.com"}).to_html()

    print(test_leaf_node)
    print(test_leaf_node2)

main()