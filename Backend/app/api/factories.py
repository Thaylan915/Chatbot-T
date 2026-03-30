from Backend.app.application.login_admin import LoginAdmin
from Backend.app.application.delete_document import DeleteDocument
from Backend.app.application.list_documents import ListDocuments
from Backend.app.application.create_document import CreateDocument
from Backend.app.application.update_document import UpdateDocument
from Backend.app.application.create_user import CreateUser
from Backend.app.application.list_users import ListUsers
from Backend.app.application.update_user import UpdateUser
from Backend.app.application.delete_user import DeleteUser
from Backend.app.infrastructure.repositories.sql.postgres_document_repository import (
    PostgresDocumentRepository,
)
from Backend.app.infrastructure.repositories.sql.postgres_user_repository import (
    PostgresUserRepository,
)


class AuthFactory:
    @staticmethod
    def make_login() -> LoginAdmin:
        return LoginAdmin()


class DocumentFactory:

    @staticmethod
    def make_list() -> ListDocuments:
        return ListDocuments(repository=PostgresDocumentRepository())

    @staticmethod
    def make_create() -> CreateDocument:
        return CreateDocument(repository=PostgresDocumentRepository())

    @staticmethod
    def make_update() -> UpdateDocument:
        return UpdateDocument(repository=PostgresDocumentRepository())

    @staticmethod
    def make_delete() -> DeleteDocument:
        return DeleteDocument(repository=PostgresDocumentRepository())


class UserFactory:
    @staticmethod
    def make_create() -> CreateUser:
        return CreateUser(repository=PostgresUserRepository())

    @staticmethod
    def make_list() -> ListUsers:
        return ListUsers(repository=PostgresUserRepository())

    @staticmethod
    def make_update() -> UpdateUser:
        return UpdateUser(repository=PostgresUserRepository())

    @staticmethod
    def make_delete() -> DeleteUser:
        return DeleteUser(repository=PostgresUserRepository())
