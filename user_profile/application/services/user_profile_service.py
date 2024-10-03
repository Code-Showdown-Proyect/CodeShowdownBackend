import httpx
from typing import Optional

from user_profile.domain.entities.user_profile import UserProfile
from user_profile.domain.repositories.user_profile_repository import UserProfileRepository


class UserProfileService:
    def __init__(self, profile_repository: UserProfileRepository, auth_service_url: str):
        self.profile_repository = profile_repository
        self.auth_service_url = "http://127.0.0.1:8000/auth/users"

    def get_user_info_from_auth(self, user_id: int):
        # Endpoint de obtener información de usuario por ID
        url = f"{self.auth_service_url}/{user_id}"
        try:
            response = httpx.get(url)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise ValueError(f"Error fetching user data: {e.response.status_code} {e.response.text}")

    def create_profile(self, user_id: int, first_name: Optional[str] = None, last_name: Optional[str] = None,
                       description: Optional[str] = None, profile_picture_url: Optional[str] = None) -> UserProfile:
        # Obtener la información del usuario desde Auth
        user_info = self.get_user_info_from_auth(user_id)
        if not user_info:
            raise ValueError("User not found in Auth")

        profile = UserProfile(
            id=None,
            user_id=user_id,
            first_name=first_name,
            last_name=last_name,
            description=description,
            profile_picture_url=profile_picture_url
        )
        self.profile_repository.create(profile)
        return profile

    def update_profile(self, user_id: int, first_name: Optional[str] = None, last_name: Optional[str] = None,
                       description: Optional[str] = None, profile_picture_url: Optional[str] = None) -> None:
        profile = self.profile_repository.find_by_user_id(user_id)
        if not profile:
            raise ValueError("Profile not found")

        # Solo actualizamos los campos proporcionados
        if first_name:
            profile.first_name = first_name
        if last_name:
            profile.last_name = last_name
        if description:
            profile.description = description
        if profile_picture_url:
            profile.profile_picture_url = profile_picture_url

        self.profile_repository.update(profile)