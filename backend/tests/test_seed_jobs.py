import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.seed.seed_jobs import build_mock_job_postings


class SeedJobsTests(unittest.TestCase):
    def test_build_mock_job_postings_generates_enough_records(self) -> None:
        postings = build_mock_job_postings(100)

        self.assertEqual(len(postings), 100)
        self.assertTrue(all(posting["company_name"] for posting in postings))
        self.assertTrue(all(posting["title"] for posting in postings))
        self.assertTrue(all(posting["location"] for posting in postings))
        self.assertTrue(all(posting["experience"] for posting in postings))
        self.assertTrue(all(posting["skills"] for posting in postings))
        self.assertTrue(all(posting["deadline"] for posting in postings))
        self.assertTrue(all(posting["source_site"] for posting in postings))
        self.assertTrue(all(posting["description"] for posting in postings))

        categories = {posting["category"] for posting in postings}
        self.assertTrue(categories.issuperset({
            "AI 개발자",
            "백엔드 개발자",
            "프론트엔드 개발자",
            "데이터 엔지니어",
            "데이터 분석가",
            "MES 개발자",
            "기획자",
        }))


if __name__ == "__main__":
    unittest.main()
