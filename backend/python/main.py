from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from typing import List, Dict
import os
import httpx

app = FastAPI()

# Setup paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_DIR = os.path.join(BASE_DIR, "..", "frontend", "static")
TEMPLATES_DIR = os.path.join(BASE_DIR, "..", "frontend", "templates")

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

@app.get("/api/search")
async def search(q: str) -> List[Dict]:
    # Match mock results format
    return [
        {
            "title": f"Result for {q}",
            "url": "https://example.com",
            "description": "Sample description",
            "source": "Sample Dataset"
        }
    ]

@app.get("/results", response_class=HTMLResponse)
async def results(request: Request, q: str):
    # Mock search results
    mock_results = [
        {
            "title": "My Hero Academia - Official Wiki",
            "url": "https://myheroacademia.fandom.com/",
            "description": "My Hero Academia is a Japanese superhero manga series written and illustrated by Kōhei Horikoshi.",
            "source": "Anime Dataset"
        },
        {
            "title": "Watch My Hero Academia | Netflix",
            "url": "https://www.netflix.com/title/my-hero-academia",
            "description": "In a world where 80% of the population has superpowers, teenager Izuku Midoriya must study at a prestigious hero academy without any powers of his own.",
            "source": "Streaming Dataset"
        },
        {
            "title": "My Hero Academia - Latest News",
            "url": "https://www.animenews.com/mha",
            "description": "Get the latest updates on My Hero Academia Season 7, manga chapters, and upcoming movie releases.",
            "source": "News Dataset"
        }
    ]

    return templates.TemplateResponse("results.html", {
        "request": request,
        "query": q,
        "results": mock_results
    })


@app.get("/api/search")
async def search(q: str) -> List[Dict]:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"http://localhost:8080/api/java/search?query={q}")
        return response.json()