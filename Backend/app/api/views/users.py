"""
Views para operações CRUD de usuários.
Usa UserFactory (Factory Method) para obter os casos de uso.
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from Backend.app.api.factories import UserFactory
from Backend.app.api.permissions import IsAdminProfile


class UserListView(APIView):
    """
    GET  /api/users/  — Lista todos os usuários (apenas admin).
    POST /api/users/  — Cria um novo usuário (aberto para auto-cadastro).
    """

    def get_permissions(self):
        if self.request.method == "POST":
            return [AllowAny()]
        return [IsAdminProfile()]

    def get(self, request):
        caso_de_uso = UserFactory.make_list()
        resultado = caso_de_uso.executar()
        return Response({"usuarios": resultado}, status=status.HTTP_200_OK)

    def post(self, request):
        first_name = request.data.get("nome", "").strip()
        email = request.data.get("email", "").strip()
        password = request.data.get("senha", "")

        caso_de_uso = UserFactory.make_create()

        try:
            resultado = caso_de_uso.executar(
                first_name=first_name,
                email=email,
                password=password,
            )
            return Response(resultado, status=status.HTTP_201_CREATED)

        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserDetailView(APIView):
    """
    PATCH  /api/users/<id>/  — Atualiza dados de um usuário (apenas admin).
    DELETE /api/users/<id>/  — Remove um usuário (apenas admin).
    """

    permission_classes = [IsAdminProfile]

    def patch(self, request, user_id: int):
        first_name = request.data.get("nome") or None
        email = request.data.get("email") or None
        password = request.data.get("senha") or None
        is_staff = request.data.get("is_staff")
        is_active = request.data.get("is_active")

        # Converte strings para bool se necessário
        if isinstance(is_staff, str):
            is_staff = is_staff.lower() == "true"
        if isinstance(is_active, str):
            is_active = is_active.lower() == "true"

        # Mantém None quando não enviado
        if "is_staff" not in request.data:
            is_staff = None
        if "is_active" not in request.data:
            is_active = None

        caso_de_uso = UserFactory.make_update()

        try:
            resultado = caso_de_uso.executar(
                user_id=user_id,
                first_name=first_name,
                email=email,
                password=password,
                is_staff=is_staff,
                is_active=is_active,
            )
            return Response(resultado, status=status.HTTP_200_OK)

        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        except LookupError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, user_id: int):
        caso_de_uso = UserFactory.make_delete()

        try:
            resultado = caso_de_uso.executar(
                user_id=user_id,
                requesting_user_id=request.user.id,
            )
            return Response(resultado, status=status.HTTP_200_OK)

        except PermissionError as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)

        except LookupError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
