from pathlib import Path

from flask import Flask, jsonify, request
from flask_cors import CORS

from .experiment import run_experiment
from .validation import ValidationError, parse_experiment_request


def create_app() -> Flask:
    backend_dir = Path(__file__).resolve().parents[1]
    app = Flask(__name__, static_folder=str(backend_dir / "static"), static_url_path="/static")
    app.config["JSON_SORT_KEYS"] = False
    app.config["GENERATED_IMAGE_DIR"] = backend_dir / "static" / "generated"

    CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.errorhandler(ValidationError)
    def handle_validation_error(error: ValidationError):
        return jsonify({"error": str(error)}), 400

    @app.get("/")
    def index():
        return jsonify(
            {
                "project": "Online Graph Coloring Analysis API",
                "status": "ok",
                "endpoints": ["/api/health", "/api/experiments", "/api/graph-coloring"],
            }
        )

    @app.get("/api/health")
    def health():
        return jsonify({"status": "ok"})

    @app.post("/api/experiments")
    def experiments():
        experiment_request = parse_experiment_request(request.get_json(silent=True))
        result = run_experiment(experiment_request, Path(app.config["GENERATED_IMAGE_DIR"]))
        return jsonify(result.to_dict())

    @app.post("/api/graph-coloring")
    def legacy_graph_coloring():
        return experiments()

    return app
