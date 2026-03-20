from pathlib import Path

from graph_coloring.experiment import run_experiment
from graph_coloring.models import ExperimentRequest


SCENARIOS = [
    (
        "CBIP on bipartite graphs",
        ExperimentRequest(
            chromatic_number=2,
            number_of_vertices=30,
            number_of_instances=20,
            coloring_method="cbip",
            edge_probability=0.45,
            seed=42,
        ),
    ),
    (
        "First Fit on bipartite graphs",
        ExperimentRequest(
            chromatic_number=2,
            number_of_vertices=30,
            number_of_instances=20,
            coloring_method="first_fit",
            edge_probability=0.45,
            seed=42,
        ),
    ),
    (
        "First Fit on 3-partite graphs",
        ExperimentRequest(
            chromatic_number=3,
            number_of_vertices=30,
            number_of_instances=20,
            coloring_method="first_fit",
            edge_probability=0.35,
            seed=42,
        ),
    ),
    (
        "First Fit on 4-partite graphs",
        ExperimentRequest(
            chromatic_number=4,
            number_of_vertices=36,
            number_of_instances=20,
            coloring_method="first_fit",
            edge_probability=0.35,
            seed=42,
        ),
    ),
]


def main():
    output_dir = Path(__file__).resolve().parent / "static" / "generated"

    header = "| Scenario | Avg colors | Avg ratio | Avg runtime (ms) | Best ratio | Worst ratio |"
    divider = "| --- | ---: | ---: | ---: | ---: | ---: |"
    print(header)
    print(divider)

    for scenario_name, request in SCENARIOS:
        result = run_experiment(request, output_dir)
        summary = result.summary
        print(
            "| "
            f"{scenario_name} | "
            f"{summary.average_colors_used} | "
            f"{summary.average_ratio} | "
            f"{summary.average_runtime_ms} | "
            f"{summary.best_ratio} | "
            f"{summary.worst_ratio} |"
        )


if __name__ == "__main__":
    main()
