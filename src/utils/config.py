import yaml
from pathlib import Path

def load_config(config_path: str) -> dict:
    """Load configuration from a YAML file."""
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    return config