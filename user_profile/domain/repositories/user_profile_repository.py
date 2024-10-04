from abc import ABC, abstractmethod
from typing import Optional

from user_profile.domain.entities.user_profile import UserProfile


class UserProfileRepository(ABC):

    @abstractmethod
    def find_by_user_id(self, user_id: int) -> Optional[UserProfile]:
        raise NotImplementedError

    @abstractmethod
    def create(self, profile: UserProfile) -> None:
        raise NotImplementedError

    @abstractmethod
    def update(self, profile: UserProfile) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete(self, profile: UserProfile) -> None:
        raise NotImplementedError

