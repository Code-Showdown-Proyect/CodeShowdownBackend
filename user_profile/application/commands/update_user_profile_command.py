from typing import Optional


class UpdateUserProfileCommand:
    def __init__(self, user_id: int, first_name: Optional[str] = None, last_name: Optional[str] = None,
                 profile_picture: Optional[str] = None, description: Optional[str] = None):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.profile_picture = profile_picture
        self.description = description