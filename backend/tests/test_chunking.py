import unittest

from backend.chunking import split_text


class TestSplitText(unittest.TestCase):
    def test_empty_text_returns_no_chunks(self):
        self.assertEqual(split_text(""), [])

    def test_text_shorter_than_size_returns_one_unchanged_chunk(self):
        text = "short text"

        self.assertEqual(split_text(text, size=20, overlap=5), [text])

    def test_text_exactly_size_returns_one_chunk(self):
        text = "a" * 10

        self.assertEqual(split_text(text, size=10, overlap=3), [text])

    def test_1254_character_text_returns_three_chunks(self):
        chunks = split_text("a" * 1254)

        self.assertEqual(len(chunks), 3)

    def test_consecutive_chunks_overlap_by_exactly_overlap_characters(self):
        overlap = 100
        chunks = split_text(
            "abcdefghijklmnopqrstuvwxyz" * 60, size=500, overlap=overlap
        )

        self.assertTrue(
            all(
                previous[-overlap:] == following[:overlap]
                for previous, following in zip(chunks, chunks[1:])
            )
        )

    def test_no_chunk_exceeds_size(self):
        size = 500
        chunks = split_text("abcdefghijklmnopqrstuvwxyz" * 60, size=size, overlap=100)

        self.assertTrue(all(len(chunk) <= size for chunk in chunks))

    def test_removing_overlaps_reconstructs_original_text(self):
        text = "abcdefghijklmnopqrstuvwxyz" * 60
        overlap = 100
        chunks = split_text(text, size=500, overlap=overlap)

        reconstructed = chunks[0] + "".join(chunk[overlap:] for chunk in chunks[1:])

        self.assertEqual(reconstructed, text)

    def test_overlap_equal_to_or_greater_than_size_raises_value_error(self):
        with self.assertRaises(ValueError):
            split_text("some text", size=5, overlap=5)

        with self.assertRaises(ValueError):
            split_text("some text", size=5, overlap=6)
