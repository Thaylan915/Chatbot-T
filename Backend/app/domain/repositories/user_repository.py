from abc import ABC, abstractmethod


class UserRepository(ABC):

    @abstractmethod
    def get_by_id(self, user_id: int):
        """Retorna um usuário pelo ID ou None se não existir."""
        pass

    @abstractmethod
    def get_by_email(self, email: str):
        """Retorna um usuário pelo e-mail ou None se não existir."""
        pass

    @abstractmethod
    def list_all(self) -> list:
        """Retorna todos os usuários cadastrados."""
        pass

    @abstractmethod
    def save(self, first_name: str, email: str, password: str) -> dict:
        """
        Cria um novo usuário.
        Retorna um dict com os dados do usuário criado.
        """
        pass

    @abstractmethod
    def update(self, user_id: int, campos: dict) -> dict | None:
        """
        Atualiza campos de um usuário existente.
        Retorna um dict com os dados atualizados ou None se não encontrado.
        """
        pass

    @abstractmethod
    def delete(self, user_id: int) -> bool:
        """
        Remove um usuário.
        Retorna True se removido, False se não encontrado.
        """
        pass
