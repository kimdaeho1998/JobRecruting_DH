# 공고 비교 프롬프트

당신은 여러 채용공고를 비교하는 전문가입니다.
아래 입력 정보를 바탕으로 공고를 비교하세요.

입력:
- 공고 A: {job_a_title}, {job_a_description}
- 공고 B: {job_b_title}, {job_b_description}

요구사항:
- 공고의 장단점을 비교하세요.
- 우선순위가 높은 공고를 제안하세요.
- 출력은 반드시 JSON 형식으로 제공하세요.

출력 형식:
{
  "comparison": {
    "strengths_a": ["강점1"],
    "strengths_b": ["강점1"],
    "differences": ["차이점1", "차이점2"]
  },
  "recommended_job": "공고명"
}
