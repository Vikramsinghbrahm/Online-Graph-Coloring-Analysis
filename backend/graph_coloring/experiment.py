import random
from pathlib import Path
from time import perf_counter

from .algorithms import color_graph, is_valid_coloring
from .generator import generate_k_partite_graph
from .models import ExperimentResult, ExperimentSummary, InstanceResult
from .visualization import render_graph_image


def _round_metric(value: float) -> float:
    return round(value, 4)


def run_experiment(request, output_dir: Path) -> ExperimentResult:
    base_seed = request.seed if request.seed is not None else random.randint(1, 1_000_000_000)
    instances: list[InstanceResult] = []
    valid_colorings = True
    sample_graph = None
    sample_coloring = None
    sample_seed = base_seed

    for index in range(request.number_of_instances):
        instance_seed = base_seed + index
        rng = random.Random(instance_seed)
        graph, _partition_map = generate_k_partite_graph(
            num_vertices=request.number_of_vertices,
            partition_count=request.chromatic_number,
            rng=rng,
            edge_probability=request.edge_probability,
        )

        start_time = perf_counter()
        coloring = color_graph(graph, request.coloring_method)
        runtime_ms = (perf_counter() - start_time) * 1000

        coloring_is_valid = is_valid_coloring(graph, coloring)
        valid_colorings = valid_colorings and coloring_is_valid

        colors_used = len(set(coloring.values()))
        ratio = colors_used / request.chromatic_number
        instances.append(
            InstanceResult(
                instance=index + 1,
                seed=instance_seed,
                colors_used=colors_used,
                ratio=_round_metric(ratio),
                runtime_ms=_round_metric(runtime_ms),
            )
        )

        if sample_graph is None:
            sample_graph = graph
            sample_coloring = coloring
            sample_seed = instance_seed

    summary = ExperimentSummary(
        average_colors_used=_round_metric(sum(instance.colors_used for instance in instances) / len(instances)),
        average_ratio=_round_metric(sum(instance.ratio for instance in instances) / len(instances)),
        average_runtime_ms=_round_metric(sum(instance.runtime_ms for instance in instances) / len(instances)),
        best_ratio=_round_metric(min(instance.ratio for instance in instances)),
        worst_ratio=_round_metric(max(instance.ratio for instance in instances)),
        valid_colorings=valid_colorings,
    )

    image_name = render_graph_image(sample_graph, sample_coloring, output_dir)
    edge_count = sum(len(neighbors) for neighbors in sample_graph.values()) // 2

    return ExperimentResult(
        request=request,
        summary=summary,
        instances=instances,
        sample_graph={
            "image": image_name,
            "imageUrl": f"/static/generated/{image_name}",
            "seed": sample_seed,
            "vertexCount": len(sample_graph),
            "edgeCount": edge_count,
        },
    )
