from dotenv import load_dotenv
from pathlib import Path
import os

filepath = Path(__file__).resolve()
dotenv_path = filepath.parent.parent / "credentials.env"
load_dotenv(dotenv_path)


env_credentials = {
    "CLIENT_ID": os.environ.get("CLIENT_ID"),
    "CLIENT_SECRET": os.environ.get("CLIENT_SECRET"),
    "REFRESH_TOKEN": os.environ.get("REFRESH_TOKEN"),
}

for key, value in env_credentials.items():
    if env_credentials[key] is None:
        raise ValueError(f"{key} is missing from credentials.env")

CLIENT_ID = env_credentials["CLIENT_ID"]
CLIENT_SECRET = env_credentials["CLIENT_SECRET"]
REFRESH_TOKEN = env_credentials["REFRESH_TOKEN"]