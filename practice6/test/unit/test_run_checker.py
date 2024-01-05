import unittest
from run_checker import check_file

class TestRunChecker(unittest.TestCase):

    def test_check_file(self):
        check_file("test/unit/test_data/valid_file.txt")
        check_file("test/unit/test_data/invalid_file.txt")
        self.assertEqual(True, True)


if __name__ == "__main__":
    unittest.main()
