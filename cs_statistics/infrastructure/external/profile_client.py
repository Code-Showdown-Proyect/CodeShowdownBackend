import httpx


class ProfileClient:
    def __init__(self, profile_service_url: str):
        self.profile_service_url = profile_service_url

    def get_user_profile(self, user_id: int):
        url = f"{self.profile_service_url}/profiles/{user_id}"
        try:
            response = httpx.get(url)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise ValueError(f"Error fetching profile data: {e.response.status_code} {e.response.text}")