"""Train the local anomaly model."""

from nsms.config import Config
from nsms.monitoring import train_model


if __name__ == "__main__":
    config = Config.load()
    train_model(config)
    print("Model trained and saved")
