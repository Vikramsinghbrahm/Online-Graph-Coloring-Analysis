# Online Graph Coloring Analysis

Online Graph Coloring Analysis is a full-stack application for running and comparing online graph coloring experiments on randomly generated k-partite graphs.

The repository includes:

- a Flask API for experiment execution and result delivery
- a Vue dashboard for configuring runs and reviewing output
- benchmark scenarios for repeatable comparisons
- automated tests for core backend behavior

## Overview

Graph coloring assigns labels to vertices such that adjacent vertices do not share the same color. This project focuses on the online setting, where coloring decisions are made as vertices are revealed.

The application supports:

- random k-partite graph generation
- multiple coloring strategies, including First Fit and CBIP
- per-run metrics for colors used, ratio to target chromatic number, and runtime
- rendered sample graphs for visual inspection
- reproducible runs through fixed seeds

## Architecture

### Backend

`backend/graph_coloring/`

- `api.py`: Flask app factory and route definitions
- `validation.py`: request parsing and domain constraints
- `generator.py`: k-partite graph generation
- `algorithms.py`: First Fit and CBIP implementations
- `experiment.py`: experiment execution and metric aggregation
- `visualization.py`: graph rendering
- `models.py`: experiment result models

### Frontend

`frontend/src/`

- `components/LandingPage.vue`: product overview
- `components/GraphColoring.vue`: experiment workbench
- `config.js`: API configuration
- `assets/styles.css`: application styles

## Results Snapshot

The benchmark table below was generated on March 20, 2026 using:

- fixed seed `42`
- `20` instances per scenario
- `python backend/benchmark.py`

| Scenario | Avg colors | Avg ratio | Avg runtime (ms) | Best ratio | Worst ratio |
| --- | ---: | ---: | ---: | ---: | ---: |
| CBIP on bipartite graphs | 3.1 | 1.55 | 1.2904 | 1.0 | 2.0 |
| First Fit on bipartite graphs | 3.35 | 1.675 | 0.0611 | 1.0 | 3.0 |
| First Fit on 3-partite graphs | 5.25 | 1.75 | 0.0293 | 1.3333 | 2.0 |
| First Fit on 4-partite graphs | 6.7 | 1.675 | 0.0355 | 1.5 | 2.0 |

Key observations:

- CBIP used fewer colors than First Fit on the same bipartite benchmark.
- First Fit remained substantially faster because of its simpler greedy rule.
- On higher-partite graph families, First Fit stayed fast but continued to exceed the target chromatic number.

## Verification

The following checks were executed successfully:

- `python -m pytest backend/tests -q`
- `npm run lint`
- `npm run build`
- `python backend/benchmark.py`

Backend test result:

- `7 passed`

## Local Setup

### Python environment

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
```

### Frontend dependencies

```powershell
cd frontend
npm install
cd ..
```

### Start the backend

```powershell
.\.venv\Scripts\python.exe backend/app.py
```

The API is available at `http://localhost:5000`.

### Start the frontend

Optional local environment file:

```powershell
Copy-Item frontend\.env.example frontend\.env.local
```

Run the frontend:

```powershell
cd frontend
npm run serve
cd ..
```

The web application is available at `http://localhost:8080`.

## API

### Health Check

`GET /api/health`

```json
{
  "status": "ok"
}
```

### Run An Experiment

`POST /api/experiments`

Request body:

```json
{
  "chromaticNumber": 3,
  "numberOfVertices": 24,
  "numberOfInstances": 8,
  "coloringMethod": "first_fit",
  "edgeProbability": 0.35,
  "seed": 42
}
```

Response shape:

```json
{
  "request": {
    "chromatic_number": 3,
    "number_of_vertices": 24,
    "number_of_instances": 8,
    "coloring_method": "first_fit",
    "edge_probability": 0.35,
    "seed": 42
  },
  "summary": {
    "average_colors_used": 5.0,
    "average_ratio": 1.6667,
    "average_runtime_ms": 0.03,
    "best_ratio": 1.3333,
    "worst_ratio": 2.0,
    "valid_colorings": true
  },
  "instances": [
    {
      "instance": 1,
      "seed": 42,
      "colors_used": 5,
      "ratio": 1.6667,
      "runtime_ms": 0.03
    }
  ],
  "sample_graph": {
    "image": "graph_xxxxx.png",
    "imageUrl": "/static/generated/graph_xxxxx.png",
    "seed": 42,
    "vertexCount": 24,
    "edgeCount": 76
  }
}
```

## Project Structure

```text
.
|-- backend/
|   |-- app.py
|   |-- benchmark.py
|   |-- graph_coloring/
|   |-- static/generated/
|   `-- tests/
|-- frontend/
|   |-- public/
|   |-- src/
|   `-- .env.example
|-- requirements.txt
|-- requirements-dev.txt
`-- README.md
```

## Notes

- The API validates domain-specific constraints, including restricting CBIP requests to bipartite graph families.
- Production frontend dependencies were updated so `npm audit --omit=dev` reports zero vulnerabilities as of March 20, 2026.
- A future migration from Vue CLI to Vite would modernize the frontend toolchain further.
