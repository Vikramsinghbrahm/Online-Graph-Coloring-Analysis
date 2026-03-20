from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class ExperimentRequest:
    chromatic_number: int
    number_of_vertices: int
    number_of_instances: int
    coloring_method: str
    edge_probability: float
    seed: int | None = None


@dataclass(frozen=True)
class InstanceResult:
    instance: int
    seed: int
    colors_used: int
    ratio: float
    runtime_ms: float


@dataclass(frozen=True)
class ExperimentSummary:
    average_colors_used: float
    average_ratio: float
    average_runtime_ms: float
    best_ratio: float
    worst_ratio: float
    valid_colorings: bool


@dataclass(frozen=True)
class ExperimentResult:
    request: ExperimentRequest
    summary: ExperimentSummary
    instances: list[InstanceResult]
    sample_graph: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["method"] = self.request.coloring_method
        payload["average"] = self.summary.average_ratio
        payload["image"] = self.sample_graph.get("image")
        return payload
