"""
Caso de uso: criar um novo usuário.
"""

from Backend.app.domain.repositories.user_repository import UserRepository


class CreateUser:

    def __init__(self, repository: UserRepository):
        self._repository = repository

    def executar(self, first_name: str, email: str, password: str) -> dict:
        if not first_name or not first_name.strip():
            raise ValueError("O campo 'nome' é obrigatório.")

        if not email or not email.strip():
            raise ValueError("O campo 'e-mail' é obrigatório.")

        if not password or len(password) < 6:
            raise ValueError("A senha deve ter no mínimo 6 caracteres.")

        if self._repository.get_by_email(email.strip()):
            raise ValueError("Já existe um usuário com este e-mail.")

        return self._repository.save(
            first_name=first_name.strip(),
            email=email.strip(),
            password=password,
        )
