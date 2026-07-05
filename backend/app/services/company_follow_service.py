from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models import CompanyFollow
from app.repositories.company_follow_repository import CompanyFollowRepository
from app.repositories.company_repository import CompanyRepository
from app.repositories.user_repository import UserRepository


class CompanyFollowService:
    def __init__(self, db: Session) -> None:
        self.repository = CompanyFollowRepository(db)
        self.company_repository = CompanyRepository(db)
        self.user_repository = UserRepository(db)

    def add_company_follow(self, user_id: int, company_id: int) -> CompanyFollow:
        self.user_repository.ensure_user(user_id)
        if not self.company_repository.get_by_id(company_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")

        follow = self.repository.get_by_user_and_company(user_id, company_id)
        if follow:
            return follow

        return self.repository.add(CompanyFollow(user_id=user_id, company_id=company_id))

    def delete_company_follow(self, user_id: int, company_id: int) -> None:
        follow = self.repository.get_by_user_and_company(user_id, company_id)
        if not follow:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company follow not found")
        self.repository.delete(follow)
