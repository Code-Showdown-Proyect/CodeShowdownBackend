from abc import abstractmethod, ABC

from competition.domain.entities.answer import Answer


class AnswerRepository(ABC):

    @abstractmethod
    def create(self, answer: Answer) -> None:
        pass
