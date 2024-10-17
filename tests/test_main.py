import unittest
import numpy as np
from src.main import vectorize_paragraphs, remove_similar_sentences

class TestMainModule(unittest.TestCase):

    def test_vectorize_paragraphs(self):
        paragraphs = [
            "This is the first sentence.",
            "This is the second sentence.",
            "Here is another different sentence."
        ]
        vectors, vectorizer = vectorize_paragraphs(paragraphs)
        
        # Test if the output is a sparse matrix
        self.assertEqual(vectors.shape[0], len(paragraphs))
        self.assertGreater(vectors.shape[1], 0)
        self.assertIsNotNone(vectorizer)
    
    def test_remove_similar_sentences(self):
        sentences = [
            "This is a sentence.",
            "This is a very similar sentence.",
            "Completely different sentence here."
        ]
        unique_sentences = remove_similar_sentences(sentences, threshold=0.8)
        
        # Test that similar sentences are removed
        self.assertEqual(len(unique_sentences), 3)
        self.assertIn("Completely different sentence here.", unique_sentences)
        self.assertIn("This is a sentence.", unique_sentences)
        self.assertIn("This is a very similar sentence.", unique_sentences)

if __name__ == '__main__':
    unittest.main()