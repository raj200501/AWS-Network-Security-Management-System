import unittest
from pathlib import Path

from nsms.model import AnomalyModel
from nsms.model_io import load_model, save_model
from nsms.preprocessing import FeatureVector


class TestModelIO(unittest.TestCase):
    def test_save_and_load_model(self):
        model = AnomalyModel.train([FeatureVector(100.0, 0, 0, 0)])
        model_path = Path("outputs") / "model-io.json"
        save_model(model, model_path)
        loaded = load_model(model_path)
        self.assertEqual(loaded.threshold, model.threshold)
        self.assertEqual(loaded.stats.mean_bytes, model.stats.mean_bytes)


if __name__ == "__main__":
    unittest.main()
