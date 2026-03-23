import logging
from time import perf_counter
from uuid import uuid4

from pathlib import Path

from flask import Flask, g, jsonify, request
from flask_cors import CORS
from werkzeug.exceptions import HTTPException

from .config import load_config
from .experiment import run_experiment
from .logging_utils import configure_logging
from .metrics import MetricsRegistry
from .validation import ValidationError, parse_experiment_request

logger = logging.getLogger(__name__)


def create_app() -> Flask:
    backend_dir = Path(__file__).resolve().parents[1]
    app_config = load_config(backend_dir)
    configure_logging(app_config.app_log_level)

    app = Flask(__name__, static_folder=str(backend_dir / "static"), static_url_path="/static")
    app.config["JSON_SORT_KEYS"] = False
    app.config["GENERATED_IMAGE_DIR"] = app_config.generated_image_dir
    app.config["APP_HOST"] = app_config.app_host
    app.config["APP_PORT"] = app_config.app_port
    app.config["APP_DEBUG"] = app_config.app_debug
    app.config["APP_REQUEST_ID_HEADER"] = app_config.request_id_header
    app.extensions["metrics"] = MetricsRegistry()

    CORS(app, resources={r"/api/*": {"origins": app_config.cors_origins}})

    @app.before_request
    def start_request_timer():
        g.request_started_at = perf_counter()
        g.request_id = request.headers.get(app.config["APP_REQUEST_ID_HEADER"], str(uuid4()))

    @app.after_request
    def track_request(response):
        duration_ms = round((perf_counter() - getattr(g, "request_started_at", perf_counter())) * 1000, 4)
        request_id = getattr(g, "request_id", str(uuid4()))
        response.headers[app.config["APP_REQUEST_ID_HEADER"]] = request_id

        app.extensions["metrics"].record_request(request.path, response.status_code, duration_ms)
        logger.info(
            "request.completed",
            extra={
                "request_id": request_id,
                "path": request.path,
                "method": request.method,
                "status_code": response.status_code,
                "duration_ms": duration_ms,
                "remote_addr": request.remote_addr,
            },
        )
        return response

    @app.errorhandler(ValidationError)
    def handle_validation_error(error: ValidationError):
        return jsonify({"error": str(error), "requestId": getattr(g, "request_id", None)}), 400

    @app.errorhandler(Exception)
    def handle_unexpected_error(error: Exception):
        if isinstance(error, HTTPException):
            return error

        logger.exception(
            "request.failed",
            extra={
                "request_id": getattr(g, "request_id", None),
                "path": request.path if request else None,
                "method": request.method if request else None,
            },
        )
        return jsonify({"error": "Internal server error", "requestId": getattr(g, "request_id", None)}), 500

    @app.get("/")
    def index():
        return jsonify(
            {
                "project": "Online Graph Coloring Analysis API",
                "status": "ok",
                "endpoints": ["/api/health", "/api/metrics", "/api/experiments", "/api/graph-coloring"],
            }
        )

    @app.get("/api/health")
    def health():
        return jsonify({"status": "ok", "requestId": getattr(g, "request_id", None)})

    @app.get("/api/metrics")
    def metrics():
        return jsonify(app.extensions["metrics"].snapshot())

    @app.post("/api/experiments")
    def experiments():
        experiment_request = parse_experiment_request(request.get_json(silent=True))
        result = run_experiment(experiment_request, Path(app.config["GENERATED_IMAGE_DIR"]))
        app.extensions["metrics"].record_experiment(
            experiment_request.coloring_method,
            result.summary.average_ratio,
        )
        return jsonify(result.to_dict())

    @app.post("/api/graph-coloring")
    def legacy_graph_coloring():
        return experiments()

    return app
