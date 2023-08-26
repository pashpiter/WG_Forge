from pathlib import Path

import yaml

BASE_DIR = Path(__file__).parent
config_path = BASE_DIR / 'config.yaml'


def get_yaml(path: Path) -> dict:
    with open(path) as f:
        return yaml.safe_load(f)


config = get_yaml(config_path)
