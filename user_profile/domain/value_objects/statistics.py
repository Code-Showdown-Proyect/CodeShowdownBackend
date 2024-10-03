class Statistics:
    def __init__(self, total_score: int = 0, competitions_won: int = 0, challenges_completed: int = 0):
        self.total_score = total_score
        self.competitions_won = competitions_won
        self.challenges_completed = challenges_completed

    def __repr__(self):
        return f"Statistics(total_score={self.total_score}, competitions_won={self.competitions_won}, challenges_completed={self.challenges_completed})"

    def update_score(self, score: int) -> None:
        self.total_score += score

    def increment_competitions_won(self) -> None:
        self.competitions_won += 1

    def increment_challenges_completed(self) -> None:
        self.challenges_completed += 1