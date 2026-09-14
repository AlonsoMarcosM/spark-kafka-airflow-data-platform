import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_portfolio_manifest_v2_and_evidence_paths():
    manifest = json.loads((ROOT / "portfolio.json").read_text(encoding="utf-8"))
    required = {
        "schema_version", "repository", "repository_url", "slug", "title",
        "lifecycle", "classification", "problem", "architecture", "dataFlow",
        "stack", "team", "ownership", "verifiedMetrics", "evidence", "assets",
        "limitations", "links",
    }
    assert manifest["schema_version"] == 2
    assert required.issubset(manifest)
    assert {link["type"] for link in manifest["links"]} >= {"technical_docs", "case_study", "github"}
    for item in manifest["evidence"]:
        assert (ROOT / item["path"]).exists(), item["path"]

