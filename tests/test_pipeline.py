import unittest
from pathlib import Path

from nsms.config import Config
from nsms.monitoring import run_pipeline, train_model


class TestPipeline(unittest.TestCase):
    def test_pipeline_writes_outputs(self):
        config = Config.load()
        temp_dir = Path("outputs") / "test-temp"
        temp_dir.mkdir(parents=True, exist_ok=True)
        config = config.from_mapping(
            {
                **config.__dict__,
                "output_dir": str(temp_dir),
                "model_path": str(temp_dir / "model.json"),
            }
        )
        model = train_model(config)
        output_dir = run_pipeline(config, model=model)
        self.assertTrue((output_dir / "alerts.jsonl").exists())
        self.assertTrue((output_dir / "metrics.json").exists())


if __name__ == "__main__":
    unittest.main()
