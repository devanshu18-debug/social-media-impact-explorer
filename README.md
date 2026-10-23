# Social Media Impact Explorer

A small educational website for exploring model predictions from student behavior inputs. It serves a plain HTML/CSS/JavaScript frontend and a FastAPI backend from one site.

## Run locally

Use Python 3.12. From this folder:

1. Create a virtual environment: `py -3.12 -m venv .venv`
2. Install packages: `.venv\Scripts\python.exe -m pip install -r requirements.txt`
3. Start the app without auto-reload: `.venv\Scripts\python.exe -m uvicorn main:app`
4. Open http://127.0.0.1:8000

Interactive API documentation is at http://127.0.0.1:8000/docs.

## Deploy on Render

This repository includes render.yaml. In Render, create a new Blueprint and connect this GitHub repository. Render reads the service settings from render.yaml. The service runs the API and website together.

Alternatively, create a Web Service with:
- Build command: pip install -r requirements.txt
- Start command: uvicorn main:app --host 0.0.0.0 --port $PORT
- Health check path: /health

The model file and social_media_model.py must be in the repository root. The raw CSV and notebook are intentionally excluded from the deployment package.

## Data and limitations

The demo processes a prediction request in memory and does not save submitted form values. Model estimates reflect patterns in the supplied observational dataset; they do not establish cause and effect and are not a health diagnosis.
