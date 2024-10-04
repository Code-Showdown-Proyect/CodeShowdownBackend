import httpx

class FeedbackClient:
    def __init__(self, feedback_service_url: str):
        self.feedback_service_url = feedback_service_url

    def get_feedback_statistics(self, user_id: int):
        url = f"{self.feedback_service_url}/feedback/{user_id}"
        try:
            response = httpx.get(url)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise ValueError(f"Error fetching feedback data: {e.response.status_code} {e.response.text}")