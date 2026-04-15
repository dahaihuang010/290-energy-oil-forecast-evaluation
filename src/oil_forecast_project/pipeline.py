from __future__ import annotations

from pathlib import Path

import pandas as pd

from oil_forecast_project.analysis.models import fit_rolling_models
from oil_forecast_project.analysis.plots import plot_benchmark_metrics, plot_eia_vintages, plot_model_comparison
from oil_forecast_project.config import OUTPUTS_DIR
from oil_forecast_project.datasets import build_eia_forecast_dataset, build_evaluation_panel, write_benchmark_summary
from oil_forecast_project.io import write_excel


def _write_project_summary(
    benchmark_metrics: pd.DataFrame,
    rolling_metrics: pd.DataFrame,
    panel: pd.DataFrame,
) -> Path:
    summary_lines = [
        "# Oil Forecast Evaluation Summary",
        "",
        "## Main dataset",
        f"- EIA Brent vintages: {panel['vintage_year'].nunique()} publication years used in realized evaluation",
        f"- Forecast observations used in 3y/5y evaluation: {len(panel)}",
        "",
        "## Benchmark results",
        benchmark_metrics.to_string(index=False),
        "",
        "## Rolling model results",
        rolling_metrics.to_string(index=False) if not rolling_metrics.empty else "No rolling model metrics were generated.",
        "",
        "## Notes",
        "- Main analysis uses EIA Brent Spot forecasts from AEO Table 12, deflated to 2025 dollars with CPI.",
        "- Realized annual Brent prices come from FRED DCOILBRENTEU aggregated to annual averages.",
        "- The market-augmented model uses Brent front-month futures from Yahoo Finance (`BZ=F`) as a market-information proxy.",
        "- World Bank archive data are downloaded as supplementary material because the forecast object is `Crude oil, avg`, not exact Brent.",
    ]
    path = OUTPUTS_DIR / "project_summary.md"
    path.write_text("\n".join(summary_lines))
    return path


def run_pipeline() -> None:
    bundle = build_eia_forecast_dataset()
    panel = build_evaluation_panel(bundle["eia"])
    benchmark_metrics = write_benchmark_summary(panel)
    rolling_predictions, rolling_metrics = fit_rolling_models(bundle["actual"], bundle["release_features"])

    plot_eia_vintages(panel, bundle["actual"])
    plot_benchmark_metrics(benchmark_metrics)
    if not rolling_metrics.empty:
        plot_model_comparison(rolling_metrics)
    _write_project_summary(benchmark_metrics, rolling_metrics, panel)

    write_excel(
        OUTPUTS_DIR / "analysis_outputs.xlsx",
        {
            "eia_eval_panel": panel,
            "benchmark_metrics": benchmark_metrics,
            "rolling_predictions": rolling_predictions,
            "rolling_metrics": rolling_metrics,
            "actual_brent": bundle["actual"],
            "eia_full": bundle["eia"],
            "world_bank": bundle["world_bank"],
        },
    )
