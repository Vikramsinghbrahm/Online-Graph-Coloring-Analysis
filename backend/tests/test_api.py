from pathlib import Path

import pytest

from graph_coloring.api import create_app


@pytest.fixture()
def client(tmp_path: Path):
    app = create_app()
    app.config["TESTING"] = True
    app.config["GENERATED_IMAGE_DIR"] = tmp_path / "generated"

    with app.test_client() as test_client:
        yield test_client


def test_healthcheck_returns_ok(client):
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_experiment_returns_structured_response(client):
    response = client.post(
        "/api/experiments",
        json={
            "chromaticNumber": 3,
            "numberOfVertices": 15,
            "numberOfInstances": 4,
            "coloringMethod": "first_fit",
            "edgeProbability": 0.35,
            "seed": 17,
        },
    )

    payload = response.get_json()

    assert response.status_code == 200
    assert payload["summary"]["valid_colorings"] is True
    assert payload["summary"]["average_ratio"] >= 1
    assert payload["sample_graph"]["image"].endswith(".png")
    assert len(payload["instances"]) == 4


def test_cbip_validation_rejects_non_bipartite_requests(client):
    response = client.post(
        "/api/experiments",
        json={
            "chromaticNumber": 3,
            "numberOfVertices": 12,
            "numberOfInstances": 3,
            "coloringMethod": "cbip",
        },
    )

    payload = response.get_json()

    assert response.status_code == 400
    assert "bipartite" in payload["error"].lower()
