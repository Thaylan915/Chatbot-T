"""
Implementação PostgreSQL do repositório de usuários.
Repository Pattern — ConcreteRepository usando Django ORM + User embutido do Django.
"""

from django.contrib.auth.models import User

from Backend.app.domain.repositories.user_repository import UserRepository


class PostgresUserRepository(UserRepository):

    def get_by_id(self, user_id: int):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None

    def get_by_email(self, email: str):
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None

    def list_all(self) -> list:
        return list(
            User.objects.all().values(
                "id", "first_name", "email", "is_staff", "is_active", "date_joined"
            )
        )

    def save(self, first_name: str, email: str, password: str) -> dict:
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=first_name,
        )
        return {
            "id": user.id,
            "first_name": user.first_name,
            "email": user.email,
            "is_staff": user.is_staff,
            "is_active": user.is_active,
            "date_joined": user.date_joined.isoformat(),
        }

    def update(self, user_id: int, campos: dict) -> dict | None:
        user = self.get_by_id(user_id)
        if user is None:
            return None

        campos_permitidos = {"first_name", "email", "is_staff", "is_active"}
        for campo, valor in campos.items():
            if campo in campos_permitidos:
                setattr(user, campo, valor)
                if campo == "email":
                    user.username = valor

        if "password" in campos and campos["password"]:
            user.set_password(campos["password"])

        user.save()

        return {
            "id": user.id,
            "first_name": user.first_name,
            "email": user.email,
            "is_staff": user.is_staff,
            "is_active": user.is_active,
        }

    def delete(self, user_id: int) -> bool:
        user = self.get_by_id(user_id)
        if user is None:
            return False
        user.delete()
        return True
