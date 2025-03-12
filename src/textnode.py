from enum import Enum

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINKS= "links"
    IMAGES = "image"

class TextNode:
    def __init__(self, text, text_type:TextType, url=None):
        self.text = text
        self.text_type = text_type 
        self.url = url
        
            
    def __eq__(self, node2) -> bool:
        if not isinstance(node2, TextNode):
            return False
        
        return (
            self.text == node2.text and 
            self.text_type == node2.text_type and
            self.url == node2.url
        )
            
    def __repr__(self):
        text = f"TextNode({self.text}, {self.text_type.value}, {self.url})"
        return text
        
    