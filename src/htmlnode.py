from textnode import TextType

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")

    def props_to_html(self):
        if self.props is None:
            return ""
        props_html = ""
        for prop in self.props:
            props_html += f' {prop}="{self.props[prop]}"'
        return props_html

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, value, tag = None, props=None):
        super().__init__(tag=tag, value=value,children= None, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError("invalid HTML: no value")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props)
        self.counter = 0
        self.value = ""
        self.value_children = ""
        
    def to_html(self):
        
        if not self.tag:
            raise ValueError("Tag should be entered")
        
        if not self.children:
            raise ValueError("Parent node must have children nodes")
        
        def build_children_html(index = 0 , accumulated =""):
            if index == len(self.children):
                return accumulated

            child_html = self.children[index].to_html()
            
            return build_children_html(index + 1, accumulated + child_html)

        children_html = build_children_html()
        return f"<{self.tag}>{children_html}</{self.tag}>"
    
    
    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"   
    

def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(value=f"{text_node.text}")
    elif text_node.text_type == TextType.BOLD:
        return LeafNode(tag="b",value=f"{text_node.text}")
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode(tag="i",value=f"{text_node.text}")
    elif text_node.text_type == TextType.CODE:
        return LeafNode(tag="code",value=f"{text_node.text}")
    elif text_node.text_type == TextType.LINKS:
        return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
    elif text_node.text_type == TextType.IMAGES:
        return LeafNode(tag="img", value="", props={"src": text_node.url, "alt": text_node.text})
    
    raise Exception(f"Text type should be one of the following: {TextType._member_names_}")    
    