"""
Token JWT customizado que injeta o perfil do usuário no payload.
Ao decodificar o token no frontend é possível ler o campo 'perfil'
sem uma chamada extra à API.
"""

from rest_framework_simplejwt.tokens import RefreshToken


class CustomRefreshToken(RefreshToken):
    @classmethod
    def for_user(cls, user):
        token = super().for_user(user)
        token["perfil"] = "admin" if user.is_staff else "usuario"
        token["nome"] = user.first_name or user.username
        token["email"] = user.email
        return token
