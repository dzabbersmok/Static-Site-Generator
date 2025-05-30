import unittest

from textnode import TextType, TextNode
from functions import split_nodes_delimiter

class TestFunctions(unittest.TestCase):
    def test_bold(self):
        node = TextNode("This is **bold text** line!", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

        text = new_nodes[1].text
        text_type = new_nodes[1].text_type
        new_nodes_len = len(new_nodes)

        self.assertEqual(text, "bold text")
        self.assertEqual(new_nodes_len, 3)
        self.assertEqual(text_type, TextType.BOLD)

    def test_italic(self):
        node = TextNode("This is __italic text__ line!", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "__", TextType.ITALIC)

        text = new_nodes[1].text
        text_type = new_nodes[1].text_type
        new_nodes_len = len(new_nodes)

        self.assertEqual(text, "italic text")
        self.assertEqual(new_nodes_len, 3)
        self.assertEqual(text_type, TextType.ITALIC)

    def test_code(self):
        node = TextNode("This is `code text` line!", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        text = new_nodes[1].text
        text_type = new_nodes[1].text_type
        new_nodes_len = len(new_nodes)

        self.assertEqual(text, "code text")
        self.assertEqual(new_nodes_len, 3)
        self.assertEqual(text_type, TextType.CODE)

    def test_multiple_bold_sections(self):
        node = TextNode("This is **bold text 1** with another **bold text 2**!", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

        text1 = new_nodes[1].text
        text2 = new_nodes[3].text
        text_type = new_nodes[1].text_type
        new_nodes_len = len(new_nodes)

        self.assertEqual(text1, "bold text 1")
        self.assertEqual(text2, "bold text 2")
        self.assertEqual(new_nodes_len, 5)
        self.assertEqual(text_type, TextType.BOLD)
        
    def test_no_delimiters(self):
        node = TextNode("This is text line!", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.TEXT)

        text = new_nodes[0].text
        text_type = new_nodes[0].text_type
        new_nodes_len = len(new_nodes)

        self.assertEqual(text, "This is text line!")
        self.assertEqual(new_nodes_len, 1)
        self.assertEqual(text_type, TextType.TEXT)

    def test_unmatched_delimiter(self):
        node = TextNode("This is **bold text 1** with another **bold text 2!", TextType.TEXT)
        with self.assertRaises(Exception) as context:
            split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertTrue("Odd number (3) of delimiter!" in str(context.exception))

    def test_text_starts_with_delimiter(self):
        node = TextNode("**This line starts with bold text** and ends with normal text!", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

        text = new_nodes[0].text
        text1 = new_nodes[1].text
        new_nodes_len = len(new_nodes)

        self.assertEqual(text, "")
        self.assertEqual(text1, "This line starts with bold text")
        self.assertEqual(new_nodes_len, 3)

    def test_text_ends_with_delimiter(self):
        node = TextNode("This line starts with normal text and ends with **bold text!**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
 
        text = new_nodes[0].text
        text1 = new_nodes[2].text
        new_nodes_len = len(new_nodes)

        self.assertEqual(text, "This line starts with normal text and ends with ")
        self.assertEqual(text1, "")
        self.assertEqual(new_nodes_len, 3)

if __name__ == "__main__":
    unittest.main()