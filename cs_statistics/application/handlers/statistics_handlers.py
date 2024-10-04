from cs_statistics.application.commands.statistics_commands import UpdateStatisticsCommand, CreateStatisticsCommand
from cs_statistics.domain.entities.statistics import CompetitionStatistics
from cs_statistics.domain.repositories.statistics_repository import StatisticsRepository


class UpdateStatisticsHandler:
    def __int__(self, statistics_repository: StatisticsRepository):
        self.statistics_repository = statistics_repository

    def handle(self, command: UpdateStatisticsCommand):
        #obtener las estadísticas actuales del usuario
        user_statistics = self.statistics_repository.get_competition_statistics(command.user_id)

        if not user_statistics:
            raise ValueError(f"User with id {command.user_id} does not have any statistics")

        #actualizar las estadísticas con los valores proporcionados en el comando
        if command.competitions_completed is not None:
            user_statistics.competitions_completed = command.competitions_completed
        if command.total_score is not None:
            user_statistics.total_score = command.total_score
        if command.average_time_per_question is not None:
            user_statistics.average_time_per_question = command.average_time_per_question
        if command.average_time_per_competition is not None:
            user_statistics.average_time_per_competition = command.average_time_per_competition

        #guardar los cambios en el repo

        self.statistics_repository.save_competition_statistics(user_statistics)

class CreateStatisticsHandler:
    def __init__(self, statistics_repository: StatisticsRepository):
        self.statistics_repository = statistics_repository

    def handle(self, command: CreateStatisticsCommand):
        #Crear una nueva instancia de edstadisticas para el usuario
        new_statistics = CompetitionStatistics(
            user_id=command.user_id,
            competitions_completed=0,
            average_score= 0.0,
            total_score=0,
            average_time_per_question=0.0,
            average_time_per_competition=0.0
        )
        self.statistics_repository.save_competition_statistics(new_statistics)
