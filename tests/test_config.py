import unittest
from pathlib import Path

from nsms.config import Config


class TestConfig(unittest.TestCase):
    def test_load_default_config(self):
        config = Config.load()
        self.assertEqual(config.data_path, Path("data/sample_logs.csv"))
        self.assertEqual(config.output_dir, Path("outputs"))

    def test_config_validation_accepts_threshold(self):
        config = Config.from_mapping(
            {
                "data_path": "data/sample_logs.csv",
                "threat_intel_path": "data/threat_intel.json",
                "compliance_rules_path": "data/compliance_rules.json",
                "model_path": "models/anomaly_model.json",
                "output_dir": "outputs",
                "anomaly_threshold": 1.0,
                "allowed_regions": ["us-east-1"],
                "allowed_protocols": ["HTTPS"],
                "high_risk_actions": ["DELETE"],
                "retention_days": 30,
            }
        )
        self.assertEqual(config.anomaly_threshold, 1.0)


if __name__ == "__main__":
    unittest.main()
