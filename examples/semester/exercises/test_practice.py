import unittest
from practice import total, clean_mean


class PracticeTests(unittest.TestCase):
    def test_total(self):
        self.assertEqual(total([2, 4, 6]), 12)
        self.assertEqual(total([]), 0)
        self.assertEqual(total([-2, 2]), 0)

    def test_clean_mean(self):
        self.assertEqual(clean_mean([2, None, 4, 6]), 4.0)
        self.assertEqual(clean_mean([0, None, 4]), 2.0)
        self.assertIsNone(clean_mean([None]))
        self.assertIsNone(clean_mean([]))


if __name__ == '__main__':
    unittest.main()
