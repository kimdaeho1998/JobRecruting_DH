from __future__ import annotations

import random
import sys
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.app.models import Base, Company, JobPosting, Skill, JobSkill
from backend.app.core.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

random.seed(42)

CATEGORIES = [
    "AI 개발자",
    "백엔드 개발자",
    "프론트엔드 개발자",
    "데이터 엔지니어",
    "데이터 분석가",
    "MES 개발자",
    "기획자",
]

COMPANIES = [
    "TechNova",
    "DataForge",
    "VisionWorks",
    "InnoGrid",
    "SmartFactory",
    "CloudMate",
    "AIDream",
    "FutureLab",
    "PixelOne",
    "Nexora",
]

LOCATIONS = ["서울", "부산", "대전", "대구", "인천", "원격"]
EXPERIENCE_LEVELS = ["신입", "1년차", "3년차", "5년차", "10년차 이상"]
SOURCES = ["원티드", "사람인", "잡코리아", "LinkedIn", "로켓펀치"]
SKILL_MAP = {
    "AI 개발자": ["Python", "PyTorch", "TensorFlow", "FastAPI", "MLOps"],
    "백엔드 개발자": ["Python", "Django", "FastAPI", "PostgreSQL", "AWS"],
    "프론트엔드 개발자": ["React", "TypeScript", "Next.js", "TailwindCSS", "Vite"],
    "데이터 엔지니어": ["Python", "Spark", "Airflow", "Kafka", "BigQuery"],
    "데이터 분석가": ["SQL", "Python", "Tableau", "Power BI", "A/B Testing"],
    "MES 개발자": ["C#", ".NET", "PLC", "SCADA", "FactoryIo"],
    "기획자": ["기획", "문서화", "사용자 조사", "PRD", "Jira"],
}


def build_mock_job_postings(count: int = 100) -> list[dict[str, Any]]:
    postings: list[dict[str, Any]] = []
    for index in range(1, count + 1):
        category = CATEGORIES[(index - 1) % len(CATEGORIES)]
        company_name = COMPANIES[(index - 1) % len(COMPANIES)]
        location = LOCATIONS[(index - 1) % len(LOCATIONS)]
        experience = EXPERIENCE_LEVELS[(index - 1) % len(EXPERIENCE_LEVELS)]
        skills = random.sample(SKILL_MAP[category], k=3)
        deadline = (datetime.now() + timedelta(days=(index % 45) + 5)).date()
        source_site = SOURCES[(index - 1) % len(SOURCES)]
        title = f"[{category}] {company_name} 채용"
        description = (
            f"{company_name}의 {category} 포지션입니다. "
            f"{location}에서 {experience} 수준의 인재를 모집합니다. "
            f"기술스택: {', '.join(skills)}. "
            f"서비스 기획부터 운영까지 참여할 수 있는 경험이 있는 분을 찾습니다."
        )

        postings.append(
            {
                "company_name": company_name,
                "category": category,
                "title": title,
                "location": location,
                "experience": experience,
                "skills": skills,
                "deadline": deadline,
                "source_site": source_site,
                "description": description,
            }
        )
    return postings


def seed_job_postings(count: int = 100, database_url: str | None = None) -> int:
    if database_url is None:
        database_url = settings.database_url

    if not database_url:
        raise ValueError("DATABASE_URL is not configured")

    engine = create_engine(database_url)
    if database_url.startswith("sqlite"):
        db_path = Path(database_url.replace("sqlite:///", "", 1))
        if db_path.is_absolute():
            db_path.unlink(missing_ok=True)
        else:
            (ROOT / db_path).unlink(missing_ok=True)

    with engine.begin() as connection:
        if database_url.startswith("sqlite"):
            connection.exec_driver_sql("DROP INDEX IF EXISTS ix_job_postings_company_id")
            connection.exec_driver_sql("DROP INDEX IF EXISTS ix_job_postings_title")
            connection.exec_driver_sql("DROP INDEX IF EXISTS ix_users_email")
            connection.exec_driver_sql("DROP INDEX IF EXISTS ix_resumes_user_id")
            connection.exec_driver_sql("DROP INDEX IF EXISTS ix_resume_analyses_resume_id")
            connection.exec_driver_sql("DROP INDEX IF EXISTS ix_resume_analyses_job_posting_id")
            connection.exec_driver_sql("DROP INDEX IF EXISTS ix_company_follows_company_id")
            connection.exec_driver_sql("DROP INDEX IF EXISTS ix_company_follows_user_id")
            connection.exec_driver_sql("DROP TABLE IF EXISTS job_skills")
            connection.exec_driver_sql("DROP TABLE IF EXISTS bookmarks")
            connection.exec_driver_sql("DROP TABLE IF EXISTS applications")
            connection.exec_driver_sql("DROP TABLE IF EXISTS resume_analyses")
            connection.exec_driver_sql("DROP TABLE IF EXISTS resumes")
            connection.exec_driver_sql("DROP TABLE IF EXISTS company_follows")
            connection.exec_driver_sql("DROP TABLE IF EXISTS notifications")
            connection.exec_driver_sql("DROP TABLE IF EXISTS job_postings")
            connection.exec_driver_sql("DROP TABLE IF EXISTS companies")
            connection.exec_driver_sql("DROP TABLE IF EXISTS skills")
            connection.exec_driver_sql("DROP TABLE IF EXISTS users")

    Base.metadata.create_all(engine)

    postings = build_mock_job_postings(count)
    with Session(engine) as session:
        for posting in postings:
            company = session.query(Company).filter(Company.name == posting["company_name"]).first()
            if not company:
                company = Company(name=posting["company_name"], industry="IT", website="https://example.com")
                session.add(company)
                session.flush()

            job_posting = JobPosting(
                company_id=company.id,
                title=posting["title"],
                job_category=posting["category"],
                location=posting["location"],
                experience_level=posting["experience"],
                description=posting["description"],
                salary_range="협의",
                deadline=posting["deadline"],
                source_site=posting["source_site"],
                source_url=f"https://{posting['source_site'].lower()}.example/jobs/{abs(hash(posting['title']))}",
                is_active=True,
            )
            session.add(job_posting)
            session.flush()

            for skill_name in posting["skills"]:
                skill = session.query(Skill).filter(Skill.name == skill_name).first()
                if not skill:
                    skill = Skill(name=skill_name, category=posting["category"])
                    session.add(skill)
                    session.flush()

                exists = session.query(JobSkill).filter(
                    JobSkill.job_posting_id == job_posting.id,
                    JobSkill.skill_id == skill.id,
                ).first()
                if not exists:
                    session.add(JobSkill(job_posting_id=job_posting.id, skill_id=skill.id))

        session.commit()

    return len(postings)


if __name__ == "__main__":
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 100
    inserted = seed_job_postings(count=count)
    print(f"Inserted {inserted} mock job postings")
