import requests
from env_var import CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN


class StravaApp:

    def __init__(self, client_id, client_secret, refresh_token) -> None:
        self._client_id = client_id
        self._client_secret = client_secret
        self._refresh_token = refresh_token
        self._access_token = self._request_access()

    def _request_access(self) -> str:
        endpoint = "https://www.strava.com/oauth/token"
        data = {
            "client_id": self._client_id,
            "client_secret": self._client_secret,
            "refresh_token": self._refresh_token,
            "grant_type": "refresh_token",
        }

        res = requests.post(endpoint, data=data)

        return res.json()["access_token"]


if __name__ == "__main__":
    app = StravaApp(CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN)
    print(app._access_token)
