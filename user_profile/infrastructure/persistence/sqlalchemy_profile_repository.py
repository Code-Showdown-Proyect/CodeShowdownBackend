from sqlalchemy.orm import Session

from user_profile.domain.entities.user_profile import UserProfile
from user_profile.infrastructure.persistence.models import UserProfileModel


class SQLAlchemyUserProfileRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, user_profile: UserProfile) -> UserProfile:
        profile_model = UserProfileModel(
            id=user_profile.user_id,
            first_name=user_profile.first_name,
            last_name=user_profile.last_name,
            profile_picture_url=user_profile.profile_picture_url
        )
        self.session.add(profile_model)
        self.session.commit()
        self.session.refresh(profile_model)
        user_profile.id = profile_model.id
        return user_profile

    def find_by_user_id(self, user_id: int) -> UserProfile:
        profile_model = self.session.query(UserProfileModel).filter_by(user_id=user_id).first()
        if not profile_model:
            return None
        return UserProfile(
            id=profile_model.id,
            user_id=profile_model.user_id,
            first_name=profile_model.first_name,
            last_name=profile_model.last_name,
            profile_picture_url=profile_model.profile_picture_url,
            description=profile_model.description
        )

    def update(self, user_profile: UserProfile) -> None:
        profile_model = self.session.query(UserProfileModel).filter_by(user_id=user_profile.user_id).first()
        if profile_model:
            profile_model.first_name = user_profile.first_name
            profile_model.last_name = user_profile.last_name
            profile_model.profile_picture_url = user_profile.profile_picture_url
            self.session.commit()

    def delete(self, user_id: int) -> None:
        profile_model = self.session.query(UserProfileModel).filter_by(user_id=user_id).first()
        if profile_model:
            self.session.delete(profile_model)
            self.session.commit()