from fastapi import FastAPI
from pydantic import BaseModel
from scripts.save_evaluation import save_evaluation

app = FastAPI()


class EvaluationRequest(BaseModel):
    job_id: int
    overall_score: int
    decision: str
    strengths: list
    missing_skills: list
    reasoning: str
    summary: str
    evaluated_at: str
    run_id: str


@app.post("/save-evaluation")
def create_evaluation(data: EvaluationRequest):
    result = save_evaluation(
        job_id=data.job_id,
        overall_score=data.overall_score,
        decision=data.decision,
        strengths=data.strengths,
        missing_skills=data.missing_skills,
        reasoning=data.reasoning,
        summary=data.summary,
        evaluated_at=data.evaluated_at,
        run_id=data.run_id,
    )

    return result