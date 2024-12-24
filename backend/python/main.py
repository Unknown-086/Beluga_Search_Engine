from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from typing import List, Dict
import os
import httpx
import time


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
    return templates.TemplateResponse("index.html", {"request": request})




@app.get("/results", response_class=HTMLResponse)
async def results(request: Request, q: str):
    start_time = time.time()

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Time Java request
            java_start = time.time()
            response = await client.get(f"http://localhost:8080/api/java/search?query={q}")
            java_time = time.time() - java_start
            print(f"\nQuery: '{q}'")
            print(f"Java service request time: {java_time:.3f} seconds")

            if response.status_code != 200:
                return templates.TemplateResponse("error.html", {
                    "request": request,
                    "error": f"Search service error: {response.text}"
                })

            # Time response processing
            process_start = time.time()
            search_results = response.json()
            process_time = time.time() - process_start
            print(f"Response processing time: {process_time:.3f} seconds")

            # Generate template response
            template_start = time.time()
            response = templates.TemplateResponse("results.html", {
                "request": request,
                "query": q,
                "results": search_results
            })
            template_time = time.time() - template_start
            print(f"Template rendering time: {template_time:.3f} seconds")

            total_time = time.time() - start_time
            print(f"Total request time: {total_time:.3f} seconds\n")

            return response

    except httpx.ReadTimeout:
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error": "Search timed out. Please try again."
        })
    except Exception as e:
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error": f"Search service unavailable: {str(e)}"
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