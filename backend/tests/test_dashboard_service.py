import sys
import unittest
from datetime import date, datetime, timedelta
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from backend.app.models import Base, Bookmark, Company, CompanyFollow, JobPosting, Skill, User, Application
from backend.app.services.dashboard_service import DashboardService


class DashboardServiceTests(unittest.TestCase):
    def test_get_stats_returns_dashboard_metrics(self) -> None:
        engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(engine)
        session = Session(engine)

        user = User(email="user@example.com", password_hash="hash", full_name="User")
        company = Company(name="Example")
        skill = Skill(name="Python")
        job = JobPosting(
            company=company,
            title="Backend Engineer",
            job_category="Backend",
            location="Seoul",
            deadline=date.today() + timedelta(days=3),
            is_active=True,
        )
        job.job_skills.append(type("JobSkill", (), {"skill": skill})())
        session.add_all([user, company, skill, job])
        session.flush()

        session.add(Bookmark(user_id=user.id, job_posting_id=job.id))
        session.add(Application(user_id=user.id, job_posting_id=job.id, status="지원 완료"))
        session.add(CompanyFollow(user_id=user.id, company_id=company.id))
        session.commit()

        stats = DashboardService(session).get_stats()

        self.assertEqual(stats["total_job_postings"], 1)
        self.assertEqual(stats["total_bookmarks"], 1)
        self.assertEqual(stats["total_applications"], 1)
        self.assertEqual(stats["applications_by_status"]["지원 완료"], 1)
        self.assertIn("top_skills", stats)
        self.assertIn("job_count_by_location", stats)
        self.assertIn("job_count_by_category", stats)
        self.assertIn("application_status_ratio", stats)

        session.close()


if __name__ == "__main__":
    unittest.main()
