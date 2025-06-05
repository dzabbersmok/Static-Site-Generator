# from leafnode import LeafNode
# from parentnode import ParentNode
# from textnode import TextNode, TextType, text_node_to_html_node
# from functions import split_nodes_delimiter, extract_markdown_images, split_nodes_link, text_to_textnodes, markdown_to_blocks, block_to_block_type, markdown_to_html_node
# from htmlnode import HTMLNode

from functions import markdown_to_html_node

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

    # some_text = "This is **bold_text** with an _italic_words_ and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
    # print(text_to_textnodes(some_text))

#     md = """
# This is **bolded** paragraph


# This is another paragraph with _italic_ text and `code` here
# This is the same paragraph on a new line



# - This is a list
# - with items

# """
#     markdown_to_blocks(md)
    # code_block = "```" \
    # "Block" \
    # "Block" \
    # "```"

    # quote_block = "> This is \n" \
    # "> Some \n" \
    # "> Quote \n" \
    # "> Block \n"

    # unordered_list = "- This is \n" \
    # "- An \n" \
    # "- Unordered List \n" \
    # "- Block \n"

    # ordered_list = "1. This is \n" \
    # "2. An \n" \
    # "3. Ordered List \n" \
    # "4. Block \n"
    md = """
### Some much
longer Header
on three lines!

This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

```
def hello_world():
    print("Hello, world!")
    return True
``` 

```
This **should not** be _bold or italic_
It should remain exactly as written
```

1. This is 
2. An
3. Ordered List
4. Block

"""
    # print(markdown_to_html_node(md).to_html())
    markdown_to_html_node(md)

main()