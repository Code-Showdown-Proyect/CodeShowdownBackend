# Interfaces para la persistencia, como UserRepository.
from abc import ABC, abstractmethod
from typing import Optional

from Auth.domain.entities import User
from Auth.domain.value_objects import Email


class UserRepository(ABC):
    @abstractmethod
    def find_by_email(self, email: Email) -> Optional[User]:
        pass

    @abstractmethod
    def create(self, user: User) -> None:
        pass