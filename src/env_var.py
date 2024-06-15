from dotenv import load_dotenv, find_dotenv, set_key
import os

DOTENV_FILE = find_dotenv("credentials.env")
load_dotenv(DOTENV_FILE)


def save_env(refresh_token):
    os.environ["REFRESH_TOKEN"] = refresh_token
    set_key(DOTENV_FILE, "REFRESH_TOKEN", os.environ["REFRESH_TOKEN"])


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

