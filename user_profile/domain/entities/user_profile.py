from typing import Optional

class UserProfile:
    def __init__(self, profile_id: int  , user_id: int, first_name: Optional[str] = None, last_name: Optional[str] = None,
                 description: Optional[str] = None, profile_picture_url: Optional[str] = None):
        self.id = profile_id
        self.user_id = user_id  # ID del usuario al que pertenece este perfil
        self.first_name = first_name  # Nombre del usuario (opcional)
        self.last_name = last_name  # Apellido del usuario (opcional)
        self.profile_picture_url = profile_picture_url  # URL de la imagen de perfil (opcional)
        self.description = description  # Descripción del usuario (opcional)

    def __repr__(self):
        return (f"UserProfile(id={self.id}, user_id={self.user_id}, first_name={self.first_name}, "
                f"last_name={self.last_name}, description={self.description}, profile_picture_url={self.profile_picture_url})")