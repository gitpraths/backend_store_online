import strawberry

from django.db import IntegrityError
from chowkidar.wrappers import issue_tokens_on_login, revoke_tokens_on_logout
from chowkidar.authentication import authenticate
from django.contrib.auth.models import User

import logging

logger = logging.getLogger(__name__)


@strawberry.type
class RegisterResponse:
    message: str
    success: bool


@strawberry.type
class LoginResult:
    success: bool
    username: str | None
    token: str | None
    errors: str | None


@strawberry.type
class AuthMutations:
    @strawberry.mutation
    def register(
        self, username: str, email: str, password: str, name: str
    ) -> RegisterResponse:
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=name,
            )
            return RegisterResponse(
                message=f"User {user.username} registered successfully!", success=True
            )
        except IntegrityError:
            return RegisterResponse(
                message="A user with that username or email already exists.",
                success=False,
            )

    @strawberry.mutation
    @issue_tokens_on_login
    def login(self, info, username: str, password: str) -> LoginResult:
        user = authenticate(username=username, password=password)
        if user:
            request = info.context["request"]
            jwt_access_token = request.COOKIES.get("JWT_ACCESS_TOKEN")
            return LoginResult(
                success=True,
                username=user.username,
                token=jwt_access_token,
                errors=None,
            )
        return LoginResult(success=False, token=None, errors="Invalid credentials")

    @strawberry.mutation
    @revoke_tokens_on_logout
    def logout(self, info) -> bool:
        info.context.LOGOUT_USER = True
        return True
