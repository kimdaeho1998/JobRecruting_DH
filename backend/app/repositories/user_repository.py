from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import User
from app.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self, session: Session) -> None:
        super().__init__(User, session)

    def get_by_email(self, email: str) -> User | None:
        result = self.session.execute(select(User).where(User.email == email))
        return result.scalars().first()

    def ensure_user(self, user_id: int) -> User:
        user = self.get_by_id(user_id)
        if user:
            return user

        user = User(
            id=user_id,
            email=f"demo{user_id}@jobinsight.local",
            password_hash="mock-password-hash",
            full_name=f"Demo User {user_id}",
            is_active=True,
        )
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user
