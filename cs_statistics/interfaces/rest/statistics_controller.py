from fastapi import APIRouter, Depends, HTTPException, status, Body
from typing import Optional

from pydantic import BaseModel

from cs_statistics.application.services.statistics_service import StatisticsService
from cs_statistics.domain.entities.statistics import UserStatistics
from cs_statistics.infrastructure.database import SessionLocal
from cs_statistics.infrastructure.persistence.statistics_repository import SQLAlchemyStatisticsRepository
from cs_statistics.security.authorization import get_current_user

router = APIRouter()

class CreateStatisticRequest(BaseModel):
    competition_completed: Optional[int] = None
    total_score: Optional[int] = None
    average_time_per_competition: Optional[float] = None
    average_score_per_competition: Optional[float] = None
    average_time_per_challenge: Optional[float] = None
    best_score: Optional[int] = None
    challenge_completed_count: Optional[int] = None

# Dependency to get the statistics service
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_statistics_service(db: SessionLocal = Depends(get_db)):

    statistics_repository = SQLAlchemyStatisticsRepository(db)

    return StatisticsService(statistics_repository)

@router.get("/user", response_model=dict)
def get_user_statistics(service: StatisticsService = Depends(get_statistics_service), current_user: int = Depends(get_current_user)):
    try:
        user_statistics = service.get_user_statistics(current_user)
        print("USER STATISTICS", user_statistics)
        if not user_statistics:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User statistics not found")
        return {
            "user_id": user_statistics["user_id"],
            "profile": {
                "first_name": user_statistics["profile"]["first_name"],
                "last_name": user_statistics["profile"]["last_name"],
                "description": user_statistics["profile"]["description"],
                "profile_picture_url": user_statistics["profile"]["profile_picture_url"]
            },
            "competition_stats": {
                "competitions_completed": user_statistics["user_statistics"]["total_completed"],
                "average_score": user_statistics["user_statistics"]["average_score"],
                "total_score": user_statistics["user_statistics"]["total_score"],
                "average_time_per_competition": user_statistics["user_statistics"]["average_time_per_competition"]
            },
            "performance_stats": {
                "best_score": user_statistics["user_statistics"]["best_score"],
                "average_time_per_challenge": user_statistics["user_statistics"]["average_time_per_challenge"],
                "challenge_completed_count": user_statistics["user_statistics"]["challenge_completed_count"]
            }
        }
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")


@router.post("/create-statistic", response_model=dict)
def create_statistics(request: CreateStatisticRequest , service: StatisticsService = Depends(get_statistics_service), user_id: int = Depends(get_current_user)):
    try:
        user_statistic = service.create_user_statistics(
            user_id=user_id,
            competitions_completed=request.competition_completed,
            total_score=request.total_score,
            average_time_per_competition=request.average_time_per_competition,
            average_score_per_competition=request.average_score_per_competition,
            average_time_per_challenge=request.average_time_per_challenge,
            best_score=request.best_score,
            challenge_completed_count=request.challenge_completed_count
        )

        return {"message": "Statistics created successfully", "user_id": user_statistic.user_id}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        print(f"Error creando estadísticas: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")

@router.put("/update", response_model=dict)
def update_statistics( request: CreateStatisticRequest ,service: StatisticsService = Depends(get_statistics_service), user_id: int = Depends(get_current_user)):
    try:
        # Suponemos que la lógica del servicio se encargará de actualizar las estadísticas necesarias.
        service.update_user_statistics(user_id, request.competition_completed, request.total_score, request.average_time_per_competition, request.average_score_per_competition, request.average_time_per_challenge, request.best_score, request.challenge_completed_count)
        return {"message": "Statistics updated successfully"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")

