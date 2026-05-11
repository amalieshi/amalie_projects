"""
ReportGenerator — produces HTML clinical summary reports from model
output DataFrames using Jinja2 templates.

No direct PyHealth calls — consumes output from BatchRiskScorer and
DrugSafetyChecker and renders them as HTML/Excel reports.
"""
from __future__ import annotations

import logging
from datetime import datetime
from pathlib import Path

import pandas as pd
from jinja2 import DictLoader, Environment

logger = logging.getLogger(__name__)

_RISK_SUMMARY_TEMPLATE = """
<!DOCTYPE html>
<html>
<head><title>Patient Risk Summary</title>
<style>
  body { font-family: Arial, sans-serif; margin: 2rem; }
  table { border-collapse: collapse; width: 100%; }
  th, td { border: 1px solid #ccc; padding: 8px 12px; text-align: left; }
  th { background: #f0f0f0; }
  .high { color: #c00; font-weight: bold; }
  .medium { color: #e65c00; }
  .low { color: #2a7a2a; }
</style>
</head>
<body>
<h1>Patient Risk Summary</h1>
<p>Model: <strong>{{ model_name }}</strong> &nbsp;|&nbsp; Generated: {{ generated_at }}</p>
<table>
  <thead>
    <tr><th>Patient ID</th><th>Visit ID</th><th>Risk Score</th><th>Risk Level</th><th>True Label</th></tr>
  </thead>
  <tbody>
    {% for row in rows %}
    <tr>
      <td>{{ row.patient_id }}</td>
      <td>{{ row.visit_id }}</td>
      <td>{{ "%.4f"|format(row.risk_score) }}</td>
      <td class="{{ row.risk_label }}">{{ row.risk_label | upper }}</td>
      <td>{{ row.true_label }}</td>
    </tr>
    {% endfor %}
  </tbody>
</table>
<p><em>{{ rows | length }} patients scored</em></p>
</body>
</html>
"""


class ReportGenerator:
    """Generate HTML and Excel reports from pipeline output DataFrames."""

    def __init__(self) -> None:
        self._env = Environment(
            loader=DictLoader({"risk_summary.html": _RISK_SUMMARY_TEMPLATE}),
            autoescape=True,
        )

    def generate_risk_summary(
        self, risk_df: pd.DataFrame, output_path: Path
    ) -> None:
        """Render an HTML risk summary report.

        Args:
            risk_df: DataFrame from BatchRiskScorer.score_batch()
            output_path: where to write the HTML file
        """
        template = self._env.get_template("risk_summary.html")
        html = template.render(
            model_name=risk_df["model_name"].iloc[0] if len(risk_df) else "unknown",
            generated_at=datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"),
            rows=risk_df.to_dict(orient="records"),
        )
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(html, encoding="utf-8")
        logger.info("Risk summary report written to %s", output_path)

    def generate_risk_excel(
        self, risk_df: pd.DataFrame, output_path: Path
    ) -> None:
        """Export risk scores to Excel with conditional formatting."""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
            risk_df.to_excel(writer, sheet_name="Risk Scores", index=False)
        logger.info("Risk scores Excel exported to %s", output_path)

    def generate_drug_safety_report(
        self, safety_df: pd.DataFrame, output_path: Path
    ) -> None:
        """Export drug safety interaction flags to HTML."""
        html = safety_df.to_html(index=False, classes="table", border=1)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(
            f"<html><body><h1>Drug Safety Report</h1>{html}</body></html>",
            encoding="utf-8",
        )
        logger.info("Drug safety report written to %s", output_path)
