# WAIO Crawler Tracker

The **WAIO Crawler Tracker** is a scientific benchmarking platform that proves
the efficiency of Semantic HTML for AI bots. It measures "Cognitive Effort" by
comparing traditional heuristic extraction against the WAIO framework.

📖 **[Read the Full Documentation
(DOCUMENTATION.md)](file:///Users/Sasha/Crawler Tracker WAIO/DOCUMENTATION.md)**

## Quick Start

### Fix npm cache (one-time)

```bash
sudo chown -R $(whoami):staff ~/.npm
```

### Backend

```bash
cd backend
pip install -r requirements.txt
playwright install chromium
uvicorn main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173

## Project Structure

```
├── backend/
│   ├── main.py           # FastAPI app
│   ├── bot_factory.py    # Bot simulations (GPTBot, ClaudeBot, etc.)
│   ├── extractors.py     # Heuristic vs WAIO extraction
│   ├── metrics.py        # Benchmark data classes
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.tsx       # Main dashboard
│   │   ├── App.css
│   │   └── index.css     # Tailwind styles
│   ├── package.json
│   ├── tailwind.config.js
│   └── postcss.config.js
└── test-pages/
    ├── standard.html     # No WAIO attributes
    └── waio.html         # With data-ai-* attributes
```

## API Endpoints

- `GET /api/bots` - List available bot types
- `POST /api/benchmark` - Run full comparison
- `POST /api/extract/heuristic` - Heuristic extraction only
- `POST /api/extract/waio` - WAIO extraction only

## Metrics

| Metric           | Description                     |
| ---------------- | ------------------------------- |
| `network_time`   | Time to download raw bytes      |
| `dom_load_time`  | Time to parse HTML into DOM     |
| `cognitive_time` | CPU time for content extraction |
