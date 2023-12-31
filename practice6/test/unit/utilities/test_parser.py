import sys
import unittest

from utilities.parser import parse_command_line_arguments

class TestParser(unittest.TestCase):
    """
    Make sure that the command line arguments are correctly parsed.
    """

    def test_command_line_parsing(self):
        saved_argv = sys.argv
        sys.argv = ['main.py','-i', '-t', 'nltk', '-s', '-l', '-m', 'porter', '-p', '-pc', '-r', 'bm25', '-b', '0.5', '-k', '1.2', '-sl', '0.35', '-n', '10', 'queries.csv', '-g', 'k1']

        try:
            # Appeler la fonction parse_command_line_arguments
            args = parse_command_line_arguments()

            # Vérifier les valeurs du Namespace résultant
            self.assertTrue(args.generate_index)
            self.assertEqual(args.tokenizer, 'regex')
            self.assertTrue(args.stopword)
            self.assertFalse(args.lemmer)
            self.assertEqual(args.stemmer, 'porter')
            self.assertTrue(args.plot)
            self.assertTrue(args.parallel_computing)
            self.assertEqual(args.ranking, 'bm25')
            self.assertEqual(args.b, 0.5)
            self.assertEqual(args.k1, 1.2)
            self.assertEqual(args.slope, 0.35)
            self.assertEqual(args.top_n, 10)
            self.assertEqual(args.queries_file_path, 'queries.csv')
            self.assertEqual(args.gradient_descent, 'k1')

        finally:
            sys.argv = saved_argv
        
    def test_wrong_weighting_function(self):
        saved_argv = sys.argv
        sys.argv = ['main.py', '-r', 'wrong', 'queries.csv']

        try:
            with self.assertRaises(SystemExit):
                args = parse_command_line_arguments()

        finally:
            sys.argv = saved_argv

    def test_default_values(self):
        saved_argv = sys.argv
        sys.argv = ['main.py', 'queries.csv']

        try:
            args = parse_command_line_arguments()

            self.assertFalse(args.generate_index)
            self.assertEqual(args.tokenizer, 'nltk')
            self.assertFalse(args.stopword)
            self.assertFalse(args.lemmer)
            self.assertEqual(args.stemmer, 'None')
            self.assertFalse(args.plot)
            self.assertFalse(args.parallel_computing)
            self.assertEqual(args.ranking, 'bm25')
            self.assertEqual(args.b, 0.5)
            self.assertEqual(args.k1, 1.2)
            self.assertEqual(args.slope, 0.35)
            self.assertEqual(args.top_n, 10)
            self.assertEqual(args.queries_file_path, 'queries.csv')
            self.assertEqual(args.gradient_descent, 'k1')

        finally:
            sys.argv = saved_argv

    def test_missing_positionnal_argument(self):
        saved_argv = sys.argv
        sys.argv = ['main.py']

        try:
            with self.assertRaises(SystemExit):
                parse_command_line_arguments()

        finally:
            sys.argv = saved_argv


if __name__ == '__main__':
    unittest.main()