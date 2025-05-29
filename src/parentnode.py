from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        children_string = ""
        if self.tag is None:
            raise ValueError("All parent nodes must have a tag!")
        
        if self.children is None or len(self.children) == 0:
            raise ValueError("All parent nodes must have child nodes!")

        for child in self.children:
                children_string += child.to_html()

        return f"<{self.tag}>{children_string}</{self.tag}>"
