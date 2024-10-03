from user_profile.application.commands.update_user_profile_command import UpdateUserProfileCommand
from user_profile.domain.repositories.user_profile_repository import UserProfileRepository


class UpdateUserProfileHandler:
    def __init__(self, repository: UserProfileRepository):
        self.repository = repository

    def handle(self, command: UpdateUserProfileCommand):
        user_profile = self.repository.find_by_user_id(command.user_id)
        if not user_profile:
            raise ValueError("Profile not found")

        if command.first_name:
            user_profile.first_name = command.first_name
        if command.last_name:
            user_profile.last_name = command.last_name
        if command.profile_picture:
            user_profile.profile_picture_url = command.profile_picture
        if command.description:
            user_profile.description = command.description

        self.repository.update(user_profile)