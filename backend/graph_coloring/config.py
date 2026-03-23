import os
from dataclasses import dataclass
from pathlib import Path


def _load_dotenv_if_present(project_root: Path) -> None:
    env_file = project_root / ".env"
    if not env_file.exists():
        return

    for raw_line in env_file.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip())


def _parse_bool(value: str | None, default: bool) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _parse_int(value: str | None, default: int) -> int:
    if value is None:
        return default
    return int(value)


@dataclass(frozen=True)
class AppConfig:
    app_host: str
    app_port: int
    app_debug: bool
    app_log_level: str
    cors_origins: list[str]
    request_id_header: str
    generated_image_dir: Path


def load_config(backend_dir: Path) -> AppConfig:
    _load_dotenv_if_present(backend_dir.parent)
    cors_origin_value = os.getenv("APP_CORS_ORIGINS", "http://localhost:8080")
    cors_origins = [origin.strip() for origin in cors_origin_value.split(",") if origin.strip()]

    return AppConfig(
        app_host=os.getenv("APP_HOST", "127.0.0.1"),
        app_port=_parse_int(os.getenv("APP_PORT"), 5000),
        app_debug=_parse_bool(os.getenv("APP_DEBUG"), True),
        app_log_level=os.getenv("APP_LOG_LEVEL", "INFO").upper(),
        cors_origins=cors_origins,
        request_id_header=os.getenv("APP_REQUEST_ID_HEADER", "X-Request-ID"),
        generated_image_dir=Path(os.getenv("GENERATED_IMAGE_DIR", backend_dir / "static" / "generated")),
    )
