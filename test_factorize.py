import unittest
from factorize import factorize

class TestFactorize(unittest.TestCase):
    def test_factorize(self):
        a, b, c, d = factorize(128, 255, 99999, 10651060)

        self.assertEqual(a, [1, 2, 4, 8, 16, 32, 64, 128])
        self.assertEqual(b, [1, 3, 5, 15, 17, 51, 85, 255])
        self.assertEqual(c, [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999])
        self.assertEqual(d, [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553,
                             760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060])

if __name__ == '__main__':
    unittest.main()
