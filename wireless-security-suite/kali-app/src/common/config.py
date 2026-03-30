import os
import yaml


def load_config(path: str = None) -> dict:
    default_path = path or os.path.join(os.path.dirname(__file__), "..", "config", "default.yaml")
    if not os.path.exists(default_path):
        return {}
    with open(default_path, "r", encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}
