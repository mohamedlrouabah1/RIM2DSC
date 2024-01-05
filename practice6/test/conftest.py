import sys
import os

src_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src")
test_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "mymock")

sys.path.insert(0, src_dir)
sys.path.insert(0, test_dir)