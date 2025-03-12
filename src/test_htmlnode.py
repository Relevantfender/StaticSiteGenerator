import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node
from textnode import TextType, TextNode

class TestHTMLNode(unittest.TestCase):
    
    def test_props_to_html(self):
        props = {
            "href":"https://www.google.com",
            "target":"_blank",
            }
        node1 = HTMLNode(
            tag="a",
            value="Link",
            props=props
        )
        
        with self.assertRaises(expected_exception= NotImplementedError):
            node1.to_html()
    
    def test_is_children_None(self):
        props = {
            "href":"https://www.google.com",
            "target":"_blank",
            }
        node1 = HTMLNode(
            tag="a",
            value="Link",
            props=props
        )
        
        self.assertIsNone(node1.children)
        
    def test_is_children_notNone(self):
        props = {
            "href":"https://www.google.com",
            "target":"_blank",
            }
        node1 = HTMLNode(
            tag="a",
            value="Link",
            props=props
        )
        node2 = HTMLNode(
            tag="p",
            value="Wall of text",
            children=[node1],
        )
        self.assertIsNotNone(node2.children, "List should have elements")
        self.assertEqual(len(node2.children), 1, "List should have 1 item")
        self.assertIs(node2.children[0], node1)
        
    def test_leaf_to_html_p(self):
        props =  {
            "href": "https://www.google.com"
            }
        node = LeafNode(tag="p", value="Hello, world!")
        node2 = LeafNode(tag="a", props=props, value="Click me!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
        self.assertEqual(node2.to_html(), "<a href=\"https://www.google.com\">Click me!</a>" )

    def test_to_html_with_children(self):
        child_node = LeafNode(tag="span", value="child")
        parent_node = ParentNode(tag="div", children=[child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode(tag="b", value="grandchild")
        child_node = ParentNode(tag="span", children=[grandchild_node])
        parent_node = ParentNode(tag="div", children=[child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
        
    def test_text(self):
        node = TextNode(text = "This is a text node", text_type= TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_image(self):
        node = TextNode("This is an image", TextType.IMAGES, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://www.boot.dev", "alt": "This is an image"},
        )

    def test_bold(self):
        node = TextNode("This is bold", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold")

        
        
if __name__ == "__main__":
    unittest.main()