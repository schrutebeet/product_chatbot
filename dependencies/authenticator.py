import sys
import yaml
from pathlib import Path

import src

key_dir = Path(src.__file__).parent.parent / "keys"
sys.path.append(str(key_dir))

import mail_key 
mail_key = mail_key

with open(key_dir / "postgres_keys.yaml", 'r') as f:
            credentials = yaml.safe_load(f)

class Settings:
    PROJECT_NAME: str = "Stocks"
    PROJECT_VERSION: str = "0.0.1"

    POSTGRES_USER: str = credentials["user"]
    POSTGRES_PASSWORD = credentials["password"]
    POSTGRES_HOST: str = credentials["host"]
    POSTGRES_PORT: str = credentials["port"]
    POSTGRES_DATABASE: str = credentials["database"]