from typing import Type

from sqlalchemy.orm import Session

from user_profile.domain.entities.user_profile import UserProfile
from user_profile.domain.repositories.user_profile_repository import UserProfileRepository
from user_profile.infrastructure.persistence.models import UserProfileModel


class SQLAlchemyUserProfileRepository(UserProfileRepository):
    def __init__(self, session: Session):
        self.session = session

    def create(self, user_profile: UserProfile) -> UserProfile:
        profile_model = UserProfileModel(
            user_id=user_profile.user_id,
            first_name=user_profile.first_name,
            last_name=user_profile.last_name,
            profile_picture_url=user_profile.profile_picture_url
        )
        self.session.add(profile_model)
        self.session.commit()
        self.session.refresh(profile_model)
        user_profile.id = profile_model.id
        return user_profile

    def find_by_user_id(self, user_id: int) -> Type[UserProfileModel] | None:
        return self.session.query(UserProfileModel).filter_by(user_id=user_id).first()


    def update(self, user_profile: UserProfile) -> None:
        profile_model = self.session.query(UserProfileModel).filter_by(user_id=user_profile.user_id).first()
        if profile_model:
            profile_model.first_name = user_profile.first_name
            profile_model.last_name = user_profile.last_name
            profile_model.profile_picture_url = user_profile.profile_picture_url
            profile_model.description = user_profile.description
            self.session.commit()

    def delete(self, profile_model: UserProfileModel) -> None:
        if profile_model:
            self.session.delete(profile_model)
            self.session.commit()