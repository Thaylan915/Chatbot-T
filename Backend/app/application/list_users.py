"""
Caso de uso: listar todos os usuários.
"""

from Backend.app.domain.repositories.user_repository import UserRepository


class ListUsers:

    def __init__(self, repository: UserRepository):
        self._repository = repository

    def executar(self) -> list:
        return self._repository.list_all()
