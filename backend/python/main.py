from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, FileResponse
from typing import List, Dict
import os
import httpx
import time
from math import ceil
from TextPreprocess import preprocessText
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


@app.get("/results", response_class=HTMLResponse)
async def results(request: Request, q: str, page: int = 1, source: str = all):
    start_time = time.time()

    # Validate source parameter
    if not source:
        raise HTTPException(status_code=400, detail="Source parameter is required")

    try:
        # Preprocess search query
        preprocess_start = time.time()
        processed_words = preprocessText(q)
        preprocess_time = time.time() - preprocess_start
        print(f"\nOriginal query: '{q}', Source: {source}")
        print(f"Preprocessed words: {processed_words}")
        print(f"Preprocessing time: {preprocess_time:.3f} seconds")

        if not processed_words:
            return templates.TemplateResponse("results.html", {
                "request": request,
                "query": q,
                "source": source,
                "results": [],
                "total_results": 0,
                "current_page": page,
                "total_pages": 0,
                "error": "Please enter a valid search term"
            })

        # Send request with source parameter
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

            process_start = time.time()
            data = response.json()
            process_time = time.time() - process_start
            print(f"Response processing time: {process_time:.3f} seconds")

            template_start = time.time()
            response = templates.TemplateResponse("results.html", {
                "request": request,
                "query": q,
                "source": source,
                "processed_query": " ".join(processed_words),
                "results": data.get("results", []),
                "total_results": data.get("totalResults", 0),
                "current_page": data.get("currentPage", page),
                "total_pages": data.get("totalPages", 1)
            })
            template_time = time.time() - template_start
            print(f"Template rendering time: {template_time:.3f} seconds")

            total_time = time.time() - start_time
            print(f"Total request time: {total_time:.3f} seconds\n")

            return response

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


@app.get("/js/script.js")
async def serve_js():
    headers = {
        'Cache-Control': 'public, max-age=31536000',
        'Content-Type': 'application/javascript'
    }
    return FileResponse(
        "frontend/static/js/script.js", 
        headers=headers
    )
