import sys
import os

src_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src")
test_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "test")
data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../..", "data")
stopword_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../.." "stopwords")

sys.path.insert(0, src_dir)
sys.path.insert(0, test_dir)
sys.path.insert(0, data_dir)
sys.path.insert(0, stopword_dir)