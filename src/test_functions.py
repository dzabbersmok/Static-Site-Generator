import unittest

from enums import TextType, BlockType
from textnode import TextNode
from functions import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, markdown_to_blocks, block_to_block_type

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

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([('to boot dev', 'https://www.boot.dev'), ('to youtube', 'https://www.youtube.com/@bootdotdev')], matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images_starts_with_image(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) image and another ![second image](https://i.imgur.com/3elNhQu.png) image!",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" image and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode(" image!", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_images_ends_with_image(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) OR ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" OR ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images_only_one_image(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_images_two_images_no_text(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png)![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images_no_image(self):
        node = TextNode(
            "No image here! Just some text...",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("No image here! Just some text...", TextType.TEXT)],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link to Boot.dev](https://www.boot.dev) and another [link to Google](https://www.google.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link to Boot.dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "link to Google", TextType.LINK, "https://www.google.com"
                ),
            ],
            new_nodes,
        )

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks__excessive_newlines__start(self):
        md = """




This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items

"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks__excessive_newlines__end(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items




"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks__excessive_newlines__middle(self):
        md = """
This is **bolded** paragraph




This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line






- This is a list
- with items

"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_block_type__heading(self):
        heading1 = block_to_block_type("# Heading 1")
        heading3 = block_to_block_type("### Heading 3")
        heading6 = block_to_block_type("###### Heading 6")
        paragraph = block_to_block_type("######### PARAGRAPH")

        self.assertEqual(heading1, BlockType.HEADING)
        self.assertEqual(heading3, BlockType.HEADING)
        self.assertEqual(heading6, BlockType.HEADING)
        self.assertEqual(paragraph, BlockType.PARAGRAPH)

    def test_block_to_block_type__code(self):
        code_block = "``` \n" \
            "Block \n" \
            "Block \n" \
            "```"

        self.assertEqual(block_to_block_type(code_block), BlockType.CODE)

    def test_block_to_block_type__quote(self):
        quote_block = "> This is \n" \
        "> Some \n" \
        "> Quote \n" \
        "> Block \n"

        self.assertEqual(block_to_block_type(quote_block), BlockType.QUOTE)

    def test_block_to_block_type__unordered_list(self):
        unordered_list = "- This is \n" \
        "- An \n" \
        "- Unordered List \n" \
        "- Block \n"

        self.assertEqual(block_to_block_type(unordered_list), BlockType.UNORDERED_LIST)

    def test_block_to_block_type__ordered_list(self):
        ordered_list = "1. This is \n" \
        "2. An \n" \
        "3. Ordered List \n" \
        "4. Block \n"

        self.assertEqual(block_to_block_type(ordered_list), BlockType.ORDERED_LIST)

    def test_block_to_block_type__empty_block(self):
        empty_block = ""

        self.assertEqual(block_to_block_type(empty_block), BlockType.PARAGRAPH)

    def test_block_to_block_type__extra_whitespace(self):
        extra_whitespace = "> This is \n" \
        "> Some \n" \
        "  \n" \
        "               \n" \
        "> Quote \n" \
        "> Block \n"

        self.assertEqual(block_to_block_type(extra_whitespace), BlockType.PARAGRAPH)

    def test_block_to_block_type__ordered_list_with_wrong_number(self):
        ordered_list = "1. This is \n" \
        "2. An \n" \
        "4. Ordered List \n" \
        "5. Block \n"

        self.assertEqual(block_to_block_type(ordered_list), BlockType.PARAGRAPH)

if __name__ == "__main__":
    unittest.main()