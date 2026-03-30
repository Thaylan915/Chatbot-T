"""
Caso de uso: atualizar dados de um usuário existente.
"""

from Backend.app.domain.repositories.user_repository import UserRepository


class UpdateUser:

    def __init__(self, repository: UserRepository):
        self._repository = repository

    def executar(
        self,
        user_id: int,
        first_name: str | None = None,
        email: str | None = None,
        password: str | None = None,
        is_staff: bool | None = None,
        is_active: bool | None = None,
    ) -> dict:
        if not self._repository.get_by_id(user_id):
            raise LookupError(f"Usuário com id={user_id} não encontrado.")

        if email is not None:
            existente = self._repository.get_by_email(email.strip())
            if existente and existente.id != user_id:
                raise ValueError("Este e-mail já está em uso por outro usuário.")

        if password is not None and len(password) < 6:
            raise ValueError("A senha deve ter no mínimo 6 caracteres.")

        campos = {}
        if first_name is not None:
            campos["first_name"] = first_name.strip()
        if email is not None:
            campos["email"] = email.strip()
        if password is not None:
            campos["password"] = password
        if is_staff is not None:
            campos["is_staff"] = is_staff
        if is_active is not None:
            campos["is_active"] = is_active

        if not campos:
            raise ValueError("Nenhum campo válido enviado para atualização.")

        resultado = self._repository.update(user_id, campos)
        if resultado is None:
            raise LookupError(f"Usuário com id={user_id} não encontrado.")

        return resultado
