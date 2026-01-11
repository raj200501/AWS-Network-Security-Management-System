import unittest

from nsms.model import AnomalyModel
from nsms.preprocessing import FeatureVector


class TestModel(unittest.TestCase):
    def test_model_scores_anomaly(self):
        features = [FeatureVector(100.0, 0, 0, 0), FeatureVector(120.0, 0, 0, 0)]
        model = AnomalyModel.train(features, threshold=2.0)
        self.assertTrue(model.is_anomalous(FeatureVector(10000.0, 1, 1, 1)))

    def test_model_predicts_all(self):
        features = [FeatureVector(100.0, 0, 0, 0), FeatureVector(120.0, 0, 0, 0)]
        model = AnomalyModel.train(features)
        predictions = model.predict(features)
        self.assertEqual(len(predictions), 2)


if __name__ == "__main__":
    unittest.main()
