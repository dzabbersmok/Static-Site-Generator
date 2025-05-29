import unittest

from htmlnode import HTMLNode

test_props = {
    "href": "https://www.google.com",
    "target": "_blank",
}
test_props_string = " href=\"https://www.google.com\" target=\"_blank\""

class TestHTMLNode(unittest.TestCase):
    # tag, value, children, props
    def test_eq(self):
        node = repr(HTMLNode("p", "This is a html p node"))
        node2 = repr(HTMLNode("p", "This is a html p node"))
        self.assertEqual(node, node2)

    def test_eq_props(self):
        props_to_html = HTMLNode("a", "This is a html a node", None, test_props).props_to_html()
        props_string = test_props_string
        self.assertEqual(props_to_html, props_string)

    def test_eq_none_props(self):
        props_to_html = HTMLNode("a", "This is a html a node", None, None).props_to_html()
        props_string = ""
        self.assertEqual(props_to_html, props_string)

    def test_eq_children(self):
        child1 = HTMLNode("span", "Hello")
        child2 = HTMLNode("span", "World")
        
        parent = repr(HTMLNode("div", None, [child1, child2]))
        test_output = "HTMLNode(div, None, [HTMLNode(span, Hello, None, None), HTMLNode(span, World, None, None)], None)"
        self.assertEqual(parent, test_output)

if __name__ == "__main__":
    unittest.main()