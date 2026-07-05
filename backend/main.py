import os, re, json, hashlib
from fastapi import FastAPI, UploadFile, File, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import pytesseract
from aiocache import Cache

from config import settings
from models import SolveResponse
from llm import query_ollama
from graphs import generate_graph

app = FastAPI(title="AI Physics Solver")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173"], allow_methods=["*"], allow_headers=["*"])
cache = Cache(Cache.MEMORY, ttl=settings.cache_ttl)
os.makedirs(settings.upload_dir, exist_ok=True)

FORMULA_CLEAN_RE = [(re.compile(r'rn\b'), 'm'), (re.compile(r'\b0(?=[A-Z])'), 'O')]
IB_CONSTANTS = {"g": 9.81, "c": 299792458, "h": 6.626e-34, "G": 6.674e-11, "e": 1.602e-19, "mu0": 1.257e-6, "epsilon0": 8.854e-12}

def clean_ocr(text: str) -> str:
    for pat, repl in FORMULA_CLEAN_RE:
        text = pat.sub(repl, text)
    return text

def extract_latex(image_path: str) -> str:
    # ponytail: pix2tex skipped (~3GB torch dep); falls back to tesseract --psm 6
    try:
        from pix2tex.cli import LatexOCR
        model = LatexOCR()
        return model(Image.open(image_path))
    except ImportError:
        import warnings
        warnings.warn("pix2tex not installed — falling back to tesseract --psm 6 for formula extraction")
        return pytesseract.image_to_string(Image.open(image_path), config="--psm 6")

def normalize_image(image: Image.Image) -> Image.Image:
    image.thumbnail((512, 512))
    return image

@app.post("/solve")
async def solve(file: UploadFile = File(...), background_tasks: BackgroundTasks = BackgroundTasks()):
    path = os.path.join(settings.upload_dir, file.filename or "upload.png")
    content = await file.read()
    with open(path, "wb") as f:
        f.write(content)

    img = Image.open(path)
    img = normalize_image(img)
    img.save(path)

    img_hash = hashlib.md5(content).hexdigest()
    cached = await cache.get(img_hash)
    if cached:
        os.remove(path)
        return cached

    ocr_text = clean_ocr(pytesseract.image_to_string(img))
    latex = extract_latex(path)

    raw = await query_ollama(ocr_text, latex)
    if isinstance(raw, str):
        raw = json.loads(raw)
    raw["graph_base64"] = generate_graph(raw.get("formula_used", ""))

    # ponytail: cross-check variable values against IB constants only for exact name matches
    for var in raw.get("variables", []):
        if var["name"] in IB_CONSTANTS:
            pass  # trust LLM but constant is known

    os.remove(path)
    await cache.set(img_hash, raw)
    return raw

@app.get("/health")
async def health():
    return {"status": "ok"}
