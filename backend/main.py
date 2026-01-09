"""
WAIO Crawler Tracker - FastAPI Backend
Comparative Bot Simulator for benchmarking semantic HTML extraction.
"""
import asyncio
from contextlib import asynccontextmanager
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os

from bot_factory import bot_factory, BotType, BOT_CONFIGS
from extractors import heuristic_extractor, waio_extractor
from metrics import ComparisonResult, BenchmarkMetrics


# Request/Response models
class BenchmarkRequest(BaseModel):
    url: str
    bot_type: str = "GPTBot"


class BotInfo(BaseModel):
    name: str
    user_agent: str
    is_dynamic: bool
    description: str


# Lifespan management
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle startup and shutdown events."""
    yield
    # Cleanup Playwright on shutdown
    await bot_factory.close()


# FastAPI app
app = FastAPI(
    title="AI Crawler Tracker",
    description="Predictive Extraction Engine — Visualizing how Semantic HTML (WAIO) eliminates bot ambiguity and slashes processing latency.",
    version="1.0.0",
    lifespan=lifespan
)

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {
        "service": "WAIO Crawler Tracker",
        "status": "operational",
        "version": "1.0.0"
    }


@app.get("/api/bots")
async def list_bots():
    """List all available bot types for simulation."""
    bots = []
    for bot_type, config in BOT_CONFIGS.items():
        bots.append({
            "id": bot_type.value,
            "name": config.name,
            "user_agent": config.user_agent,
            "is_dynamic": config.is_dynamic,
            "description": "JavaScript-enabled crawler" if config.is_dynamic else "Static HTML crawler"
        })
    return {"bots": bots}


@app.post("/api/benchmark")
async def run_benchmark(request: BenchmarkRequest):
    """
    Run a complete benchmark comparison on the given URL.
    
    This endpoint:
    1. Fetches the page using the selected bot simulation
    2. Runs BOTH extraction algorithms on the same DOM
    3. Returns comparison metrics proving WAIO's efficiency
    """
    # Validate bot type
    try:
        bot_type = BotType(request.bot_type)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid bot type. Available: {[b.value for b in BotType]}"
        )
    
    # Initialize comparison result
    result = ComparisonResult(
        url=request.url,
        bot_type=request.bot_type
    )
    
    try:
        # Fetch page using bot simulation
        html_content, fetch_metrics = await bot_factory.fetch_page(request.url, bot_type)
        
        # WARM-UP PASS: Run extraction once to "heat up" trafilatura and lxml caches
        # This ensures the first measured run (Standard) isn't unfairly penalized
        # by cold initialization costs that subsequent runs (WAIO) wouldn't face.
        _ = heuristic_extractor.extract(html_content)
        
        # Copy network/DOM metrics to both results (same fetch for both)
        result.heuristic_metrics.network_time = fetch_metrics.network_time
        result.heuristic_metrics.dom_load_time = fetch_metrics.dom_load_time
        result.heuristic_metrics.response_size = fetch_metrics.response_size
        result.heuristic_metrics.status_code = fetch_metrics.status_code
        result.heuristic_metrics.headers_sent = fetch_metrics.headers_sent
        
        result.waio_metrics.network_time = fetch_metrics.network_time
        result.waio_metrics.dom_load_time = fetch_metrics.dom_load_time
        result.waio_metrics.response_size = fetch_metrics.response_size
        result.waio_metrics.status_code = fetch_metrics.status_code
        result.waio_metrics.headers_sent = fetch_metrics.headers_sent
        
        # Run heuristic extraction (Algorithm A)
        heuristic_result, heuristic_time = heuristic_extractor.extract(html_content)
        result.heuristic_extraction = heuristic_result
        result.heuristic_metrics.cognitive_time = heuristic_time
        
        # Run WAIO extraction (Algorithm B)
        # We pass heuristic_time as baseline_time to ensure fair calculation if WAIO falls back
        waio_result, waio_time = waio_extractor.extract(html_content, baseline_time=heuristic_time)
        result.waio_extraction = waio_result
        result.waio_metrics.cognitive_time = waio_time
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Benchmark failed: {str(e)}"
        )
    
    return result.to_dict()


@app.post("/api/extract/heuristic")
async def extract_heuristic(request: BenchmarkRequest):
    """Run only heuristic extraction on a URL."""
    try:
        bot_type = BotType(request.bot_type)
    except ValueError:
        bot_type = BotType.GPTBOT
    
    try:
        html_content, metrics = await bot_factory.fetch_page(request.url, bot_type)
        result, cognitive_time = heuristic_extractor.extract(html_content)
        metrics.cognitive_time = cognitive_time
        
        return {
            "extraction": {
                "title": result.title,
                "summary": result.summary,
                "main_content": result.main_content[:1000] if result.main_content else None,
                "waio_detected": result.waio_detected
            },
            "metrics": metrics.to_dict()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/extract/waio")
async def extract_waio(request: BenchmarkRequest):
    """Run only WAIO extraction on a URL."""
    try:
        bot_type = BotType(request.bot_type)
    except ValueError:
        bot_type = BotType.GPTBOT
    
    try:
        html_content, metrics = await bot_factory.fetch_page(request.url, bot_type)
        result, cognitive_time = waio_extractor.extract(html_content)
        metrics.cognitive_time = cognitive_time
        
        return {
            "extraction": {
                "title": result.title,
                "summary": result.summary,
                "main_content": result.main_content[:1000] if result.main_content else None,
                "waio_detected": result.waio_detected,
                "attributes_found": result.attributes_found
            },
            "metrics": metrics.to_dict(),
            "framework_detected": result.waio_detected
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Serve static files from the 'static' directory if it exists (for production)
if os.path.exists("static"):
    app.mount("/", StaticFiles(directory="static", html=True), name="static")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
