import httpx
from config import settings

OLLAMA_URL = f"{settings.ollama_base_url}/api/generate"

SYSTEM_PROMPT = """You are an IB Physics tutor. Given OCR text and LaTeX formulas from a physics problem image, return strict JSON:
{
  "topic": "Mechanics|Waves|Electricity|Magnetism|Thermal|Nuclear",
  "formula_used": "$$F = ma$$",
  "variables": [{"name": "F", "unit": "N", "value": "10"}],
  "step_by_step_solution": ["Step 1: ..."],
  "common_ib_mistakes": ["Forgetting to convert units"],
  "practice_questions": ["Question 1: ..."]
}"""

async def query_ollama(ocr_text: str, latex: str) -> dict:
    prompt = f"OCR text:\n{ocr_text}\n\nDetected LaTeX:\n{latex}"
    payload = {
        "model": settings.ollama_model,
        "prompt": prompt,
        "system": SYSTEM_PROMPT,
        "format": "json",
        "stream": False,
        "options": {"temperature": 0.1},
    }
    async with httpx.AsyncClient(timeout=120) as client:
        resp = await client.post(OLLAMA_URL, json=payload)
        resp.raise_for_status()
        return resp.json()["response"]
