import sys
import os

# Add project root to Python path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(PROJECT_ROOT)

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, FileResponse
from typing import List, Dict
import httpx
import time
from math import ceil
from src.Lexicon.TextPreprocess import preprocessText, preprocessLanguageText


app = FastAPI()

# Setup paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR = os.path.join(BASE_DIR, "..", "frontend", "templates")
STATIC_DIR = os.path.join(BASE_DIR, "..", "frontend", "static")


# CORS and Static Files
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Mount static files with absolute path
app.mount("/static", StaticFiles(directory=STATIC_DIR, check_dir=True), name="static")

# Templates with absolute path
templates = Jinja2Templates(directory=TEMPLATES_DIR)

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request
    })

@app.get("/js/script.js")
async def serve_js():
    js_path = os.path.join(STATIC_DIR, "js", "script.js")
    if not os.path.exists(js_path):
        raise HTTPException(status_code=404, detail="JavaScript file not found")

    headers = {
        'Cache-Control': 'public, max-age=31536000',
        'Content-Type': 'application/javascript'
    }
    return FileResponse(js_path, headers=headers)

@app.get("/results", response_class=HTMLResponse)
async def results(request: Request, q: str, page: int = 1, source: str = None, lang: str = None):
    start_time = time.time()

    if not source:
        raise HTTPException(status_code=400, detail="Source parameter is required")

    if not lang:
        raise HTTPException(status_code=400, detail="Language parameter is required")
    print(lang)
    try:
        if lang == "english":
            processed_words = preprocessText(q)
        elif lang == "other":
            processed_words = preprocessLanguageText(q)
            # processed_words = preprocessText(q)

        # processed_words = preprocessText(q)
        print(f"\nOriginal query: '{q}', Source: {source}, Lang: {lang}")
        print(f"Preprocessed words: {processed_words}")

        if not processed_words:
            return templates.TemplateResponse("results.html", {
                "request": request,
                "query": q,
                "source": source,
                "lang": lang,
                "results": [],
                "total_results": 0,
                "current_page": page,
                "total_pages": 0,
                "error": "Please enter a valid search term"
            })

        async with httpx.AsyncClient(timeout=30.0) as client:
            words_param = ",".join(processed_words)
            java_start = time.time()
            response = await client.get(
                f"http://localhost:8080/api/java/search?query={words_param}&page={page}&source={source}"
            )
            java_time = time.time() - java_start
            print(f"Java service request time: {java_time:.3f} seconds")

            if response.status_code != 200:
                return templates.TemplateResponse("error.html", {
                    "request": request,
                    "error": f"Search service error: {response.text}"
                })

            data = response.json()
            template_response = templates.TemplateResponse("results.html", {
                "request": request,
                "query": q,
                "source": source,
                "lang": lang,
                "processed_query": " ".join(processed_words),
                "results": data.get("results", []),
                "total_results": data.get("totalResults", 0),
                "current_page": data.get("currentPage", page),
                "total_pages": data.get("totalPages", 1)
            })

            total_time = time.time() - start_time
            print(f"Total request time: {total_time:.3f} seconds\n")

            return template_response

    except Exception as e:
        print(f"Error processing request: {e}")
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error": f"Error processing request: {str(e)}"
        })


@app.get("/api/search")
async def search(q: str) -> List[Dict]:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"http://localhost:8080/api/java/search?query={q}")
            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail="Java service error")
            return response.json()
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Java service unavailable: {str(e)}")

