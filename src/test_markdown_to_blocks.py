import unittest
from markdown_blocks import BlockType, block_to_block_type, markdown_to_blocks, markdown_to_html_node


class TestMarkdownToHTML(unittest.TestCase):
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

    def test_markdown_to_blocks_newlines(self):
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
    def test_return_types(self):
        md= """
This is **bolded** paragraph




This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
        """
        list_types = []
        blocks = markdown_to_blocks(md)
        for block in blocks:
            block_type = block_to_block_type(block)
            list_types.append(block_type)
            
        self.assertEqual(list_types,[
            BlockType.PARAGRAPH,
            BlockType.PARAGRAPH,
            BlockType.UNORDERED_LIST
        ])
        
    def test_return_types_paragraph(self):
        md= """
#### This is **bolded** paragraph




This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
        """
        list_types = []
        blocks = markdown_to_blocks(md)
        for block in blocks:
            block_type = block_to_block_type(block)
            list_types.append(block_type)
            
        self.assertEqual(list_types,[
            BlockType.HEADING,
            BlockType.PARAGRAPH,
            BlockType.UNORDERED_LIST
        ])
    def test_return_types_orderedlist(self):
        md= """
#### This is **bolded** paragraph




This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

1. This is a list
2. with items
        """
        list_types = []
        blocks = markdown_to_blocks(md)
        for block in blocks:
            block_type = block_to_block_type(block)
            print(block_type)
            list_types.append(block_type)
            
        self.assertEqual(list_types,[
            BlockType.HEADING,
            BlockType.PARAGRAPH,
            BlockType.ORDERED_LIST
        ])
    def test_return_types_orderedlist(self):
        md= """
#### This is **bolded** paragraph



```
This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line
```


1. This is a list
2. with items
        """
        list_types = []
        blocks = markdown_to_blocks(md)
        for block in blocks:
            block_type = block_to_block_type(block)
            list_types.append(block_type)
            
        self.assertEqual(list_types,[
            BlockType.HEADING,
            BlockType.CODE,
            BlockType.ORDERED_LIST
        ])
        
    def test_block_to_block_types(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        block = "> quote\n> more quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        block = "- list\n- items"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
        block = "1. list\n2. items"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
        block = "paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )
            
            

if __name__ == "__main__":
    unittest.main()
