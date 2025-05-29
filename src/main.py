from textnode import TextNode, TextType
from htmlnode import HTMLNode

def main():
    test_text_node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    test_html_node = HTMLNode("p", "Some text", {"a": "test"}, {"href": "www.none.com"})

    print(test_text_node)
    print(test_html_node)

main()