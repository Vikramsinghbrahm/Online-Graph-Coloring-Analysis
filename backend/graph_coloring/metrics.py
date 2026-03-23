from collections import Counter
from threading import Lock


class MetricsRegistry:
    def __init__(self):
        self._lock = Lock()
        self._request_count = 0
        self._request_duration_ms_total = 0.0
        self._error_count = 0
        self._requests_by_path = Counter()
        self._experiments_total = 0
        self._experiments_by_method = Counter()
        self._experiment_ratio_total = 0.0

    def record_request(self, path: str, status_code: int, duration_ms: float) -> None:
        with self._lock:
            self._request_count += 1
            self._request_duration_ms_total += duration_ms
            self._requests_by_path[path] += 1
            if status_code >= 400:
                self._error_count += 1

    def record_experiment(self, method: str, average_ratio: float) -> None:
        with self._lock:
            self._experiments_total += 1
            self._experiments_by_method[method] += 1
            self._experiment_ratio_total += average_ratio

    def snapshot(self) -> dict:
        with self._lock:
            average_request_duration = (
                round(self._request_duration_ms_total / self._request_count, 4)
                if self._request_count
                else 0.0
            )
            average_experiment_ratio = (
                round(self._experiment_ratio_total / self._experiments_total, 4)
                if self._experiments_total
                else 0.0
            )

            return {
                "requests": {
                    "total": self._request_count,
                    "errors": self._error_count,
                    "averageDurationMs": average_request_duration,
                    "byPath": dict(self._requests_by_path),
                },
                "experiments": {
                    "total": self._experiments_total,
                    "averageRatio": average_experiment_ratio,
                    "byMethod": dict(self._experiments_by_method),
                },
            }
