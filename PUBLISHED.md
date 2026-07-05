# AI Physics Solver — Published

**Repository**: https://github.com/rudrashortguy/ai-physics-solver
**Release**: v1.0.0

## Hardware Requirements
- Ollama with `gemma2:latest` (4GB+ RAM)
- Tesseract OCR
- Python 3.12+ and Node.js 20+

## Quick Start
```bash
./run.sh                    # Backend on :8000, Frontend on :5173
```
Or Docker:
```bash
docker compose up --build
```

Note: pix2tex (LaTeX-OCR) requires torch (~3GB) and is optional. Falls back to tesseract.
