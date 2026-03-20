from collections.abc import Mapping
from typing import Any

from .models import ExperimentRequest

ALGORITHM_ALIASES = {
    "cbip": "cbip",
    "firstfit": "first_fit",
    "first_fit": "first_fit",
    "first-fit": "first_fit",
}


class ValidationError(ValueError):
    """Raised when the API receives invalid input."""


def _parse_int(value: Any, field_name: str, minimum: int | None = None, maximum: int | None = None) -> int:
    if isinstance(value, bool):
        raise ValidationError(f"{field_name} must be an integer.")

    try:
        parsed = int(value)
    except (TypeError, ValueError) as exc:
        raise ValidationError(f"{field_name} must be an integer.") from exc

    if minimum is not None and parsed < minimum:
        raise ValidationError(f"{field_name} must be at least {minimum}.")
    if maximum is not None and parsed > maximum:
        raise ValidationError(f"{field_name} must be at most {maximum}.")
    return parsed


def _parse_float(
    value: Any,
    field_name: str,
    minimum: float | None = None,
    maximum: float | None = None,
) -> float:
    if isinstance(value, bool):
        raise ValidationError(f"{field_name} must be a number.")

    try:
        parsed = float(value)
    except (TypeError, ValueError) as exc:
        raise ValidationError(f"{field_name} must be a number.") from exc

    if minimum is not None and parsed < minimum:
        raise ValidationError(f"{field_name} must be at least {minimum}.")
    if maximum is not None and parsed > maximum:
        raise ValidationError(f"{field_name} must be at most {maximum}.")
    return parsed


def parse_experiment_request(payload: Mapping[str, Any] | None) -> ExperimentRequest:
    if not isinstance(payload, Mapping):
        raise ValidationError("Request body must be a JSON object.")

    chromatic_number = _parse_int(payload.get("chromaticNumber"), "chromaticNumber", minimum=2, maximum=12)
    number_of_vertices = _parse_int(
        payload.get("numberOfVertices"),
        "numberOfVertices",
        minimum=chromatic_number,
        maximum=150,
    )
    number_of_instances = _parse_int(payload.get("numberOfInstances"), "numberOfInstances", minimum=1, maximum=100)
    edge_probability = _parse_float(payload.get("edgeProbability", 0.35), "edgeProbability", minimum=0.0, maximum=1.0)

    method_value = str(payload.get("coloringMethod", "")).strip().lower()
    coloring_method = ALGORITHM_ALIASES.get(method_value)
    if coloring_method is None:
        supported_methods = ", ".join(sorted(ALGORITHM_ALIASES))
        raise ValidationError(f"coloringMethod must be one of: {supported_methods}.")

    seed = payload.get("seed")
    if seed is not None and seed != "":
        seed = _parse_int(seed, "seed", minimum=0, maximum=2_147_483_647)
    else:
        seed = None

    if coloring_method == "cbip" and chromatic_number != 2:
        raise ValidationError("CBIP is defined for bipartite graphs, so chromaticNumber must be 2.")

    return ExperimentRequest(
        chromatic_number=chromatic_number,
        number_of_vertices=number_of_vertices,
        number_of_instances=number_of_instances,
        coloring_method=coloring_method,
        edge_probability=edge_probability,
        seed=seed,
    )
