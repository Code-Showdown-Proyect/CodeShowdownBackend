from typing import Optional

from user_profile.domain.entities.user_profile import UserProfile


class UserProfileRepository:
    def find_by_user_id(self, user_id: int) -> Optional[UserProfile]:
        raise NotImplementedError

    def create(self, profile: UserProfile) -> None:
        raise NotImplementedError

    def update(self, profile: UserProfile) -> None:
        raise NotImplementedError
    def delete(self, profile: UserProfile) -> None:
        raise NotImplementedError