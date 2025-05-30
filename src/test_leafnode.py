import unittest

from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_eq(self):
        node = repr(LeafNode("p", "This is a html p node"))
        node2 = repr(LeafNode("p", "This is a html p node"))
        self.assertEqual(node, node2)

    def test_eq_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"}).to_html()
        self.assertEqual(node, "<a href=\"https://www.google.com\">Click me!</a>")

if __name__ == "__main__":
    unittest.main()