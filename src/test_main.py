import unittest

from main import extract_title

class TestMainClass(unittest.TestCase):
    
    # def test_extract_title(self):
    #     markdown = r"./content/index.md"
        
    #     title = extract_title(markdown=markdown)
    #     self.assertEqual(title, "Tolkien Fan Club")
    
    def test_extract_title(self):
        markdown = r"./content/index.md"
        
        with self.assertRaises(Exception):
            text = extract_title(markdown)
    
if __name__ == "__main__":
    unittest.main()