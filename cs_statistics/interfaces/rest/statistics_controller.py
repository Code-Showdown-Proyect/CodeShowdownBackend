from fastapi import APIRouter, Depends, HTTPException, status
from typing import Optional
from cs_statistics.application.services.statistics_service import StatisticsService
from cs_statistics.domain.entities.statistics import UserStatistics
from cs_statistics.domain.repositories.statistics_repository import StatisticsRepository
from cs_statistics.infrastructure.database import SessionLocal
from cs_statistics.infrastructure.external.feedback_client import FeedbackClient
from cs_statistics.infrastructure.external.profile_client import ProfileClient

router = APIRouter()


# Dependency to get the statistics service
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_statistics_service(db: SessionLocal = Depends(get_db)):
    statistics_repository = StatisticsRepository()
    profile_client = ProfileClient(profile_service_url="http://example.com/profile")
    feedback_client = FeedbackClient(feedback_service_url="http://example.com/feedback")

    return StatisticsService(
        statistics_repository=statistics_repository,
        profile_client=profile_client,
        feedback_client=feedback_client
    )

@router.get("/statistics/user/{user_id}", response_model=dict)
def get_user_statistics(user_id: int, service: StatisticsService = Depends(get_statistics_service)):
    try:
        user_statistics: Optional[UserStatistics] = service.get_user_statistics(user_id)
        if not user_statistics:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User statistics not found")
        return {
            "user_id": user_statistics.user_id,
            "competition_stats": {
                "competitions_completed": user_statistics.competition_stats.competitions_completed,
                "average_score": user_statistics.competition_stats.average_score,
                "total_score": user_statistics.competition_stats.total_score,
                "average_time_per_question": user_statistics.competition_stats.average_time_per_question,
                "average_time_per_competition": user_statistics.competition_stats.average_time_per_competition
            },
            "performance_stats": {
                "average_result": user_statistics.performance_stats.average_result,
                "best_score": user_statistics.performance_stats.best_score,
                "average_time_per_challenge": user_statistics.performance_stats.average_time_per_challenge
            },
            "feedback_stats": {
                "suggestions_applied": user_statistics.feedback_stats.suggestions_applied
            }
        }
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")

@router.post("/statistics/update", response_model=dict)
def update_statistics(user_id: int, service: StatisticsService = Depends(get_statistics_service)):
    try:
        # Suponemos que la lógica del servicio se encargará de actualizar las estadísticas necesarias.
        service.update_user_statistics(user_id)
        return {"message": "Statistics updated successfully"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")