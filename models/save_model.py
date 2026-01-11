"""Helper to save a trained model."""

from nsms.config import Config
from nsms.monitoring import train_model


if __name__ == "__main__":
    config = Config.load()
    train_model(config)
    print(f"Model saved to {config.model_path}")
