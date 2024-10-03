from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from user_profile.application.services.user_profile_service import UserProfileService
from user_profile.infrastructure.database import SessionLocal
from user_profile.infrastructure.persistence.sqlalchemy_profile_repository import SQLAlchemyUserProfileRepository

router = APIRouter()

class CreateProfileRequest(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    description: Optional[str] = None
    profile_picture_url: Optional[str] = None

class UserProfileResponse(BaseModel):
    user_id: int
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    description: Optional[str] = None
    profile_picture_url: Optional[str] = None

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Dependency to get UserProfileService
def get_profile_service(db: Session = Depends(get_db)):
    profile_repository = SQLAlchemyUserProfileRepository(db)
    return UserProfileService(profile_repository)

@router.post("/profiles", response_model=dict)
def create_profile(request: CreateProfileRequest, user_id: int, service: UserProfileService = Depends(get_profile_service)):
    try:
        profile = service.create_profile(
            user_id=user_id,
            first_name=request.first_name,
            last_name=request.last_name,
            description=request.description,
            profile_picture_url=request.profile_picture_url
        )
        return {"message": "Profile created successfully", "profile_id": profile.id}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.put("/profiles/{user_id}", response_model=dict)
def update_profile(user_id: int, request: CreateProfileRequest, service: UserProfileService = Depends(get_profile_service)):
    try:
        service.update_profile(
            user_id=user_id,
            first_name=request.first_name,
            last_name=request.last_name,
            description=request.description,
            profile_picture_url=request.profile_picture_url
        )
        return {"message": "Profile updated successfully"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.get("/profiles/{user_id}", response_model=UserProfileResponse)
def get_profile(user_id: int, service: UserProfileService = Depends(get_profile_service)):
    try:
        profile = service.profile_repository.find_by_user_id(user_id)
        if not profile:
            raise ValueError("Profile not found")
        return UserProfileResponse(
            user_id=profile.user_id,
            first_name=profile.first_name,
            last_name=profile.last_name,
            description=profile.description,
            profile_picture_url=profile.profile_picture_url
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.delete("/profiles/{user_id}", response_model=dict)
def delete_profile(user_id: int, service: UserProfileService = Depends(get_profile_service)):
    try:
        service.profile_repository.delete(user_id)
        return {"message": "Profile deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))