# Online Graph Coloring Analysis

An interview-ready full-stack project for exploring online graph coloring strategies on randomly generated k-partite graphs.

The project combines:

- a Flask API for experiment orchestration
- a Vue dashboard for running and visualizing experiments
- reproducible benchmark scenarios
- automated tests and validation

## Why This Project Matters

Graph coloring is a classic algorithmic problem with practical links to scheduling, compiler register allocation, and resource assignment. This repository focuses on the online version of the problem, where vertices are colored as they are revealed rather than with full future knowledge.

That makes the project useful for interview discussion because it naturally touches:

- algorithm design and trade-offs
- API design and input validation
- reproducibility in simulation-heavy systems
- frontend/backend contracts
- repository hygiene and testing

## Architecture

### Backend

`backend/graph_coloring/`

- `api.py`: Flask app factory and API routes
- `validation.py`: request parsing and business rules
- `generator.py`: k-partite graph generation
- `algorithms.py`: First Fit and CBIP implementations
- `experiment.py`: experiment orchestration and metrics
- `visualization.py`: graph rendering
- `models.py`: typed experiment result objects

### Frontend

`frontend/src/`

- `components/LandingPage.vue`: project overview and interview framing
- `components/GraphColoring.vue`: experiment workbench and result presentation
- `config.js`: API base URL configuration
- `assets/styles.css`: application styling system

## Results Snapshot

Results below were generated on March 20, 2026 with:

- fixed seed `42`
- `20` experiment instances per scenario
- the built-in benchmark script: `python backend/benchmark.py`

| Scenario                      | Avg colors | Avg ratio | Avg runtime (ms) | Best ratio | Worst ratio |
| ----------------------------- | ---------: | --------: | ---------------: | ---------: | ----------: |
| CBIP on bipartite graphs      |        3.1 |      1.55 |           1.2904 |        1.0 |         2.0 |
| First Fit on bipartite graphs |       3.35 |     1.675 |           0.0611 |        1.0 |         3.0 |
| First Fit on 3-partite graphs |       5.25 |      1.75 |           0.0293 |     1.3333 |         2.0 |
| First Fit on 4-partite graphs |        6.7 |     1.675 |           0.0355 |        1.5 |         2.0 |

### Findings From The Results

- CBIP used fewer colors than First Fit on the same bipartite benchmark.
- First Fit was materially faster, which is expected from its simpler greedy rule.
- As the target chromatic number increased, First Fit stayed fast but consistently overshot the target coloring number.
- The project now makes those trade-offs visible and reproducible instead of anecdotal.

## Verification

The following checks were run successfully during cleanup:

- `python -m pytest backend/tests -q`
- `npm run lint`
- `npm run build`
- `python backend/benchmark.py`

Backend test result:

- `7 passed`

## Local Setup

### 1. Create a Python environment

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
```

### 2. Install frontend dependencies

```powershell
cd frontend
npm install
cd ..
```

### 3. Start the backend

```powershell
.\.venv\Scripts\python.exe backend/app.py
```

The API will start on `http://localhost:5000`.

### 4. Start the frontend

Create a local environment file if you want to override the default backend URL:

```powershell
Copy-Item frontend\.env.example frontend\.env.local
```

Then run:

```powershell
cd frontend
npm run serve
cd ..
```

The frontend development server runs on `http://localhost:8080`.

## API

### Health Check

`GET /api/health`

Response:

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

## Conclusion

The project now reads like an engineering project instead of a classroom prototype. It is suitable for portfolio use and for technical discussion around algorithms, system design decisions, validation, benchmarking, and software quality.

The best next improvement would be migrating the frontend from the older Vue CLI stack to Vite. The production dependency surface is clean, but a Vite migration would modernize the developer tooling and remove the remaining aging build-chain baggage from the interview story.
