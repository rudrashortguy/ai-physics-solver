# Deployment

## Hardware Requirements
- **Minimum**: 4GB RAM, 2 CPU cores (CPU inference only)
- **Recommended**: 8GB+ RAM, NVIDIA GPU with 4GB+ VRAM

## Dependencies
- Tesseract OCR: `brew install tesseract` (macOS) or `apt install tesseract-ocr` (Linux)
- Ollama with `gemma2:latest` pulled
- Python 3.12+
- Node.js 20+

## Local Setup
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cd ../frontend
npm install

./run.sh
```

## Docker
```bash
docker compose up --build
```
The base image is ~2GB due to PyTorch dependencies. GPU passthrough requires `nvidia-container-toolkit`.

## Notes
- pix2tex (LaTeX-OCR) is optional and requires torch (~3GB). Falls back to tesseract.
- Redis caching is skipped in local mode; aiocache.MEMORY is used by default.
