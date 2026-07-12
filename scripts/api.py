from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from pydantic import BaseModel
from scripts.save_evaluation import save_evaluation
from scripts.get_candidate import get_candidate
from scripts.get_all_candidates import get_all_candidates
from scripts.get_job import get_job
from scripts.get_all_jobs import get_all_jobs
from scripts.resume_parser import extract_text_from_pdf, extract_text_from_docx, structure_resume_with_ollama
from scripts.save_candidate import save_candidate

app = FastAPI()

class EvaluationRequest(BaseModel):
    job_id: int
    candidate_id: int
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
    return save_evaluation(
        job_id=data.job_id, candidate_id=data.candidate_id, overall_score=data.overall_score,
        decision=data.decision, strengths=data.strengths, missing_skills=data.missing_skills,
        reasoning=data.reasoning, summary=data.summary, evaluated_at=data.evaluated_at, run_id=data.run_id
    )

@app.get("/candidates")
def read_all_candidates(): 
    return get_all_candidates()

@app.get("/candidate/{candidate_id}")
def read_candidate(candidate_id: int): 
    return get_candidate(candidate_id)

@app.get("/jobs")
def read_all_jobs():
    return get_all_jobs()

@app.get("/job/{job_id}")
def read_job(job_id: int): 
    return get_job(job_id)

@app.post("/candidates/import")
async def import_candidate_resume(file: UploadFile = File(...)):
    """
    Parses a raw PDF or DOCX resume, extracts structure using Ollama,
    hashes the candidate profile, and saves the new record to the database.
    """
    filename = file.filename.lower()
    file_bytes = await file.read()
    
    # 1. Route raw extraction depending on the mimetype/extension
    try:
        if filename.endswith(".pdf"):
            raw_text = extract_text_from_pdf(file_bytes)
        elif filename.endswith(".docx"):
            raw_text = extract_text_from_docx(file_bytes)
        else:
            raise HTTPException(
                status_code=400, 
                detail="Unsupported file format. Please upload a PDF or DOCX file."
            )
    except Exception as parse_err:
        raise HTTPException(status_code=422, detail=str(parse_err))

    # 2. Extract structured schema elements using local Ollama model (Qwen2.5)
    try:
        structured_profile = await structure_resume_with_ollama(raw_text)
    except Exception as llm_err:
        raise HTTPException(status_code=502, detail=f"AI extraction failed: {str(llm_err)}")

    # 3. Commit structured information & Candidate Profile Fingerprint to SQLite
    try:
        # Resolve clean email fallback if missing from parser output
        candidate_name = structured_profile.get("name", "Unknown Candidate")
        fallback_email = f"{candidate_name.lower().replace(' ', '.')}@placeholder.nexient.ai"
        candidate_email = structured_profile.get("email") or fallback_email

        db_result = save_candidate(
            organization_id="default_org", # Placed under a default scoping tenant for backward compatibility
            name=candidate_name,
            email=candidate_email,
            skills=structured_profile.get("skills", []),
            experience=structured_profile.get("experience", ""),
            preferred_roles=structured_profile.get("preferred_roles", []),
            preferred_location=structured_profile.get("preferred_location", "")
        )
        return {
            "status": db_result["status"],
            "message": db_result["message"],
            "candidate_id": db_result["candidate_id"],
            "extracted_data": structured_profile
        }
    except Exception as db_err:
        raise HTTPException(status_code=500, detail=f"Database insert error: {str(db_err)}")