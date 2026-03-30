"""
Caso de uso: remover um usuário.
"""

from Backend.app.domain.repositories.user_repository import UserRepository


class DeleteUser:

    def __init__(self, repository: UserRepository):
        self._repository = repository

    def executar(self, user_id: int, requesting_user_id: int) -> dict:
        if user_id == requesting_user_id:
            raise PermissionError("Você não pode excluir sua própria conta.")

        usuario = self._repository.get_by_id(user_id)
        if not usuario:
            raise LookupError(f"Usuário com id={user_id} não encontrado.")

        self._repository.delete(user_id)
        return {"message": "Usuário removido com sucesso.", "id": user_id}
