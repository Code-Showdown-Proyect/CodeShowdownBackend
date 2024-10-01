from abc import ABC, abstractmethod
from typing import List, Optional
from competition.domain.entities.competition import Competition


class CompetitionRepository(ABC):

    @abstractmethod
    def create(self, competition: Competition) -> None:
        """Crea una nueva competencia en el repositorio"""
        pass

    @abstractmethod
    def find_by_id(self, competition_id: int) -> Optional[Competition]:
        """Busca una competencia por su ID"""
        pass

    @abstractmethod
    def find_by_access_code(self, access_code: str) -> Optional[Competition]:
        """Busca una competencia por su código de acceso"""
        pass

    @abstractmethod
    def list_all(self) -> List[Competition]:
        """Lista todas las competencias disponibles"""
        pass

    @abstractmethod
    def update(self, competition: Competition) -> None:
        """Actualiza una competencia existente"""
        pass

    @abstractmethod
    def delete(self, competition_id: int) -> None:
        """Elimina una competencia del repositorio"""
        pass