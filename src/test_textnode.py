import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("Different text", TextType.BOLD)
        self.assertNotEqual(node, node2)  

    def test_eq(self):
        node3 = TextNode("This is a text node", TextType.BOLD)
        node4 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node3, node4)  
        
    def test_url_none(self):
        node5 = TextNode("This is an url node", TextType.LINKS, url= "https://www.bootdev.com")
        node6 = TextNode("This is an url node", TextType.LINKS, url= "https://www.bootdev1.com")

        self.assertNotEqual(node5, node6)
        
if __name__ == "__main__":
    unittest.main()