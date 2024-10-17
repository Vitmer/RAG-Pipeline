import unittest
import fitz  # PyMuPDF
from PIL import Image
import io
import pytesseract
import re
from src.extract_and_clean import extract_text_with_ocr, pattern_digit_start, pattern_seite, pattern_minus, pattern_letter_or_dot

class TestExtractAndClean(unittest.TestCase):
    
    def test_extract_text_with_ocr(self):
        # Mock PDF creation
        pdf_path = 'test.pdf'
        # This test requires a mock PDF or a way to simulate PyMuPDF and OCR behavior
        try:
            # Check if extract_text_with_ocr runs without errors
            result = extract_text_with_ocr(pdf_path)
            self.assertIsInstance(result, str)  # The function should return a string
        except Exception as e:
            self.fail(f"extract_text_with_ocr raised an exception {e}")

    def test_pattern_digit_start(self):
        # Test cases for the regex that matches strings starting with a digit
        self.assertTrue(pattern_digit_start.match("1. Example"))
        self.assertFalse(pattern_digit_start.match("Example 1"))

    def test_pattern_seite(self):
        # Test cases for the regex that matches "Seite <number>"
        self.assertTrue(pattern_seite.match("Seite 10"))
        self.assertFalse(pattern_seite.match("Section 10"))

    def test_pattern_minus(self):
        # Test cases for the regex that matches lines starting with a minus
        self.assertTrue(pattern_minus.match("-Example"))
        self.assertFalse(pattern_minus.match("Example"))

    def test_pattern_letter_or_dot(self):
        # Test cases for the regex that matches digits followed by a letter or dot
        self.assertTrue(pattern_letter_or_dot.match("1a. Text"))
        self.assertFalse(pattern_letter_or_dot.match("1 Text"))

if __name__ == '__main__':
    unittest.main()