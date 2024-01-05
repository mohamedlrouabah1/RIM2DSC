import unittest
from models.IRrun import IRrun

class TestIRrun(unittest.TestCase):

    def test_init(self):
        # Test the initialization of IRrun
        weighting_function_name = "bm25"
        stop = ["stopword1", "stopword2"]
        stem = "porter"
        params = {"param1": "value1", "param2": "value2"}

        ir_run = IRrun(weighting_function_name, stop, stem, params)

        # Verify that attributes are set correctly
        self.assertIsNotNone(ir_run.id)
        self.assertIsNotNone(ir_run.file_path)
        self.assertEqual(ir_run.run_as_str, "")
        self.assertEqual(ir_run.run_type, 'element')  # Assuming default value

    def test_save_run(self):
        # Test the save_run method of IRrun
        weighting_function_name = "bm25"
        stop = ["stopword1", "stopword2"]
        stem = "porter"
        params = {"param1": "value1", "param2": "value2"}

        ir_run = IRrun(weighting_function_name, stop, stem, params)

        # Create a dummy run_as_str
        ir_run.run_as_str = "Dummy run result."

        # Test saving the run file
        saved = ir_run.save_run(verbose=False)
        self.assertTrue(saved)

    def test_load_last_id(self):
        # Test the load_last_id method of IRrun
        ir_run = IRrun("bm25", [], "porter", {})

        # Ensure that the default last_id is 0 if the file doesn't exist
        last_id = ir_run.load_last_id()
        self.assertEqual(last_id, 0)

    def test_create_file_path(self):
        # Test the _create_file_path method of IRrun
        weighting_function_name = "bm25"
        stop = ["stopword1", "stopword2"]
        stem = "porter"
        params = {"param1": "value1", "param2": "value2"}

        ir_run = IRrun(weighting_function_name, stop, stem, params)

        # Ensure that the file path is created correctly
        expected_file_path = f"../results/{IRrun.GROUP_NAME}_{ir_run.id}_{weighting_function_name}_{'_'.join(IRrun.GRANULARITY)}_stop{IRrun.STOPLIST_SIZE}_{stem}_param1_value1_param2_value2.txt"
        self.assertEqual(ir_run._create_file_path(weighting_function_name, stop, stem, params), expected_file_path)

if __name__ == "__main__":
    unittest.main()
