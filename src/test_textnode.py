import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_noteq_text_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("This is a normal text node", TextType.NORMAL, "https://www.boot.dev")
        node2 = TextNode("This is a normal text node", TextType.NORMAL, "https://www.boot.dev")
        self.assertEqual(node, node2)

    def test_eq_none_url(self):
        node = TextNode("This is a normal text node", TextType.NORMAL, None)
        node2 = TextNode("This is a normal text node", TextType.NORMAL, None)
        self.assertEqual(node, node2)


if __name__ == "__main__":
    unittest.main()