"""
Permission classes customizadas baseadas no perfil do usuário.

Perfis:
  admin   → is_staff=True  — acesso completo (documentos, usuários, métricas)
  usuario → is_staff=False — acesso apenas ao chat
"""

from rest_framework.permissions import BasePermission


class IsAdminProfile(BasePermission):
    """
    Permite acesso somente a usuários autenticados com perfil admin (is_staff=True).
    Substitui IsAdminUser do DRF para manter consistência com o sistema de perfis.
    """

    message = "Acesso restrito a administradores."

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.is_active
            and request.user.is_staff
        )


class IsUsuarioProfile(BasePermission):
    """
    Permite acesso a qualquer usuário autenticado e ativo, independente do perfil.
    """

    message = "Autenticação necessária."

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.is_active
        )
