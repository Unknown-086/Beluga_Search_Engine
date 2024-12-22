from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from typing import List, Dict

app = FastAPI()

# CORS and Static Files
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.mount("/static", StaticFiles(directory="../frontend/static"), name="static")

# Templates
templates = Jinja2Templates(directory="../frontend/templates")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/search")
async def search(q: str) -> List[Dict]:
    # Mock results
    return [
        {"title": f"Result for {q}", "description": "Sample description"},
        {"title": "Another result", "description": "More details here"}
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