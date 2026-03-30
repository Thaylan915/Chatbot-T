from django.contrib.auth import authenticate

from Backend.app.infrastructure.auth.custom_token import CustomRefreshToken


class LoginAdmin:
    """
    Caso de uso: autenticar um usuário (qualquer perfil) e retornar tokens JWT.
    O token inclui o claim 'perfil' (admin | usuario) para autorização no frontend.
    Factory Method — ConcreteProduct criado por AuthFactory.
    """

    def executar(self, username: str, password: str) -> dict:
        if not username or not password:
            raise ValueError("Usuário e senha são obrigatórios.")

        usuario = authenticate(username=username, password=password)

        if usuario is None:
            raise PermissionError("Credenciais inválidas.")

        if not usuario.is_active:
            raise PermissionError("Conta desativada. Entre em contato com o administrador.")

        refresh = CustomRefreshToken.for_user(usuario)

        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "username": usuario.username,
            "email": usuario.email,
            "nome": usuario.first_name or usuario.username,
            "perfil": "admin" if usuario.is_staff else "usuario",
        }