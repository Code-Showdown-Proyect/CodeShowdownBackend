import httpx
from typing import Optional

from user_profile.domain.entities.user_profile import UserProfile
from user_profile.domain.repositories.user_profile_repository import UserProfileRepository


class UserProfileService:
    def __init__(self, profile_repository: UserProfileRepository):
        self.profile_repository = profile_repository


    def create_profile(self, user_id: int, first_name: Optional[str] = None, last_name: Optional[str] = None,
                       description: Optional[str] = None, profile_picture_url: Optional[str] = None) -> UserProfile:

        existing_profile = self.profile_repository.find_by_user_id(user_id)
        if existing_profile:
            raise ValueError(f"A profile already exists for user_id {user_id}")


        profile = UserProfile(
            profile_id=None,
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

        if first_name:
            profile.first_name = first_name
        if last_name:
            profile.last_name = last_name
        if description:
            profile.description = description
        if profile_picture_url:
            profile.profile_picture_url = profile_picture_url

        self.profile_repository.update(profile)
