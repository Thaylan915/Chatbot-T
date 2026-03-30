from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from Backend.app.api.views.auth import LoginView
from Backend.app.api.views.chat import ChatView
from Backend.app.api.views.documents import (
    DocumentListView,
    DocumentCreateView,
    DocumentDetailView,
    DocumentDeleteView,
    DocumentConfirmDeleteView,
)
from Backend.app.api.views.users import UserListView, UserDetailView

urlpatterns = [
    # ── Auth ──────────────────────────────────────────────────────────────────
    path("auth/login/",   LoginView.as_view(),        name="login"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # ── Chat ──────────────────────────────────────────────────────────────────
    path("chat/", ChatView.as_view(), name="chat"),

    # ── Documents — CRUD completo ─────────────────────────────────────────────
    path("documents/",
         DocumentListView.as_view(),    name="document_list"),

    path("documents/create/",
         DocumentCreateView.as_view(),  name="document_create"),

    path("documents/<int:id_documento>/",
         DocumentDetailView.as_view(),  name="document_detail"),

    path("documents/<int:id_documento>/delete/",
         DocumentDeleteView.as_view(),  name="document_delete"),

    path("documents/<int:id_documento>/confirm/",
         DocumentConfirmDeleteView.as_view(), name="document_confirm_delete"),

    # ── Usuários — CRUD completo ──────────────────────────────────────────────
    path("users/",
         UserListView.as_view(),   name="user_list"),

    path("users/<int:user_id>/",
         UserDetailView.as_view(), name="user_detail"),
]
