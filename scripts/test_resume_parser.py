from pathlib import Path
import asyncio

from scripts.resume_parser import (
    extract_text_from_docx,
    extract_text_from_pdf,
    structure_resume_with_ollama,
)

resume = Path("resumes/test_resume.pdf")   # or .docx

with open(resume, "rb") as f:
    if resume.suffix.lower() == ".pdf":
        raw = extract_text_from_pdf(f.read())
    elif resume.suffix.lower() == ".docx":
        raw = extract_text_from_docx(f.read())
    else:
        raise ValueError(f"Unsupported file type: {resume.suffix}")

profile = asyncio.run(structure_resume_with_ollama(raw))

print(profile)