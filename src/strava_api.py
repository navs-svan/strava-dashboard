import requests
from env_var import CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN
from env_var import save_env


class StravaApp:

    def __init__(self, client_id, client_secret, refresh_token) -> None:
        self._client_id = client_id
        self._client_secret = client_secret
        self._refresh_token = refresh_token
        self._access_token = self._request_access()

    def get_all_activities(self, before=None, after=None, limit=30):
        endpoint = "https://www.strava.com/api/v3/athlete/activities"
        headers = self._auth_header()
        params = {"before": before, "after": after, "page": 1, "per_page": limit}

        # max is 200 per page
        resp_list = []
        if limit < 1:
            raise ValueError("Invalid limit value. Must be from 1 to 200")
        elif limit <= 200:
            resp = requests.get(endpoint, params=params, headers=headers)

            if resp.status_code != 200:
                resp.raise_for_status()

            resp_list.append(resp.json())
        else:
            while True:
                params["per_page"] = 200
                resp = requests.get(endpoint, params=params, headers=headers)

                if resp.status_code != 200:
                    resp.raise_for_status()

                resp_list.append(resp.json())
                if len(resp.json()) < 200:
                    break
                else:
                    params["page"] += 1

        return resp_list

    def get_athlete(self):
        endpoint = "https://www.strava.com/api/v3/athlete"
        headers = self._auth_header()
        resp = requests.get(endpoint, headers=headers)
        
        if resp.status_code != 200:
            resp.raise_for_status()

        athlete = resp.json()
        return athlete

    def get_athlete_stats(self):
        athlete_id = self.get_athlete()["id"]
        endpoint = f"https://www.strava.com/api/v3/athletes/{athlete_id}/stats"
        headers = self._auth_header()
        resp = requests.get(endpoint, headers=headers)
        

        if resp.status_code != 200:
            resp.raise_for_status()
        
        stats = resp.json()

        return stats

    def _request_access(self) -> str:

        endpoint = "https://www.strava.com/oauth/token"
        data = {
            "client_id": self._client_id,
            "client_secret": self._client_secret,
            "refresh_token": self._refresh_token,
            "grant_type": "refresh_token",
        }

        res = requests.post(endpoint, data=data)

        self._refresh_token = res.json()["refresh_token"]
        save_env(self._refresh_token)

        return res.json()["access_token"]

    def _auth_header(self) -> dict:

        return {"Authorization": f"Bearer {self._access_token}"}


if __name__ == "__main__":
    app = StravaApp(CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN)

    resp_list = app.get_all_activities(limit=10000)
    for activities in resp_list:
        for activity in activities:
            print(activity["name"], activity["id"])

    curr_athlete = app.get_athlete()
    print(curr_athlete)

    stats = app.get_athlete_stats()
    print(stats)
