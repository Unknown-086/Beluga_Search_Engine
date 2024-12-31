# Search Engine Project

A high-performance search engine with hybrid Python-Java architecture, real-time content addition, and multi-word search capabilities.

## Overview

The project implements a scalable search engine with:
- Multi-word query processing
- Real-time web content addition
- GPU-accelerated retrieval
- Source-based filtering
- Intersection-based ranking

## Tech Stack

### Backend
- **Python FastAPI**
  - Content Management
  - Web Scraping
  - Index Building
- **Spring Boot** 
  - Search Processing
  - GPU Content Retrieval
  - Result Ranking

### Frontend
- HTML/CSS/JavaScript
- Responsive Design
- Dark/Light Theme

### Storage
- CSV-based Document Store
- JSON Index Files
- Barrel Partitioning

## Directory Structure

### 1. `backend/`
java/ src/ - GPUContentRetriever.java - SearchService.java - SearchController.java python/ src/ - main.py (FastAPI) - DatasetManager.py


### 2. `frontend/`
static/ css/ - Styles js/ - Client Logic icons/ - Assets templates/

index.html
results.html
add.html


### 3. `src/`

#### Content Processing
- **CrawlingWebLinks/**
  - URL validation
  - Content extraction
  - Metadata parsing

#### Data Management  
- **ContentAddition/**
  - DatasetManager.py
  - UpdateExistingData.py
  - ContentAdditionToExistingData.py

#### Indexing
- **ForwardIndex/**
  - Document-centric indexing
  - Position tracking
  - Metadata storage

- **InvertedIndex/**
  - Word-centric indexing
  - Barrel distribution
  - Rank calculation

- **Barrels/**
  - HashBarrelMaker.py
  - RangeBarrelMaker.py
  - BarrelPathManager.py

#### Text Processing
- **Lexicon/**
  - Word ID management
  - Text preprocessing
  - Stopword removal

## Core Features

### 1. Search Processing
- Multi-word query support
- Intersection-based ranking
- GPU-accelerated retrieval
- Source filtering (Reddit/News)

### 2. Content Addition
- Real-time web scraping
- Automatic metadata extraction
- Index updates
- Duplicate detection

### 3. Ranking System
```python
rank = (title_weight * in_title + 
        desc_weight * in_description +
        freq_weight * word_frequency) * length_normalization 
```

API Endpoints
GET  /api/search?q={query}&page={page}&source={source}
POST /api/add-content
GET  /api/fetch-content?url={url}

Setup Instructions
Dependencies:
pip install -r requirements.txt
mvn clean install


Initialize:
python setup.py init
# Python/FastAPI
```python
uvicorn main:app --reload
```

# Java/Spring
```python
./mvnw spring-boot:run
```

Performance Features
Multi-threaded processing
GPU acceleration
Cached lexicon/barrel access
Optimized intersection algorithm


Data Structure
data/
  Datasets/ - Document store
  Lexicons/ - Word mappings  
  Barrels/ - Inverted index
  ForwardIndex/ - Document index
  UserContent/ - Added content


ibraries
Python
fastapi
pandas
nltk
beautifulsoup4
orjson
Java
Spring Boot
Jackson
SLF4J
Version Requirements
Python 3.10+
Java 11+
Maven 3.6+
