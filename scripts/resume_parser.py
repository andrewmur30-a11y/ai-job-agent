import io
import json
import httpx
from pypdf import PdfReader
from docx import Document

OLLAMA_URL = "http://localhost:11434/v1/chat/completions"

def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extracts raw text content from PDF file bytes."""
    try:
        reader = PdfReader(io.BytesIO(file_bytes))
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text.strip()
    except Exception as e:
        raise ValueError(f"Failed to parse PDF file: {e}")

def extract_text_from_docx(file_bytes: bytes) -> str:
    """Extracts raw text content from DOCX file bytes."""
    try:
        doc = Document(io.BytesIO(file_bytes))
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text.strip()
    except Exception as e:
        raise ValueError(f"Failed to parse DOCX file: {e}")

async def structure_resume_with_ollama(raw_text: str) -> dict:
    """
    Sends raw resume text to local Ollama (Qwen2.5) to parse into structured JSON.
    """
    if not raw_text.strip():
        raise ValueError("No extractable text found in resume.")

    prompt = f"""
    You are an expert resume parsing assistant. Analyze the following raw resume text and extract the candidate's core information.
    You must output a raw, valid JSON object matching this exact schema:
    {{
      "name": "Candidate's Full Name",
      "email": "Candidate's Email Address",
      "skills": ["Skill 1", "Skill 2", "Skill 3"],
      "experience": "A concise paragraph summarizing their overall professional experience, key companies, and years in the industry.",
      "preferred_roles": ["Role 1", "Role 2"],
      "preferred_location": "Remote, Onsite, or Hybrid preference"
    }}

    Strict Constraints:
    - Return ONLY the raw JSON object. Do not wrap it in markdown backticks or add introductory/concluding text.
    - If a field is not found, default to an empty list [] or string "". If email is missing, try to find a pattern matching an email or leave as empty string.

    Raw Resume Text:
    ---
    {raw_text}
    ---
    """

    payload = {
        "model": "qwen2.5:7b",
        "messages": [
            {
                "role": "system",
                "content": "You are a precise, data-extraction bot that outputs strict raw JSON profiles."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.1
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(OLLAMA_URL, json=payload, timeout=60.0)
            response.raise_for_status()
            
            result = response.json()
            raw_content = result["choices"][0]["message"]["content"].strip()
            
            # Safe JSON extractor in case Ollama wraps the output in markdown backticks
            if raw_content.startswith("```"):
                # Strip markdown code blocks if the LLM ignored constraints
                lines = raw_content.splitlines()
                if lines[0].startswith("```"):
                    lines = lines[1:]
                if lines[-1].startswith("```"):
                    lines = lines[:-1]
                raw_content = "\n".join(lines).strip()
            
            parsed_profile = json.loads(raw_content)
            return parsed_profile

        except httpx.ConnectError:
            raise ConnectionError("Could not connect to Ollama. Make sure Ollama is running locally.")
        except json.JSONDecodeError as e:
            raise ValueError(f"Ollama returned malformed JSON: {e}. Raw Response: {raw_content}")
        except Exception as e:
            raise RuntimeError(f"An unexpected parsing failure occurred: {e}")