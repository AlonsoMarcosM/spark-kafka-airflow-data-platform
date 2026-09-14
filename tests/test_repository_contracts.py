import ast
import csv
import json
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]


def test_python_sources_parse():
    for path in ROOT.rglob("*.py"):
        if ".git" not in path.parts:
            ast.parse(path.read_text(encoding="utf-8"), filename=str(path))


def test_source_contracts_are_present():
    with (ROOT / "productores/csv/catalogo_dataset.csv").open(encoding="utf-8") as stream:
        headers = set(next(csv.reader(stream)))
    assert {"dataset_id", "title"}.issubset(headers)

    first_event = (ROOT / "productores/kafka/events.jsonl").read_text(encoding="utf-8").splitlines()[0]
    event = json.loads(first_event)
    assert {"dataset_id", "event_type"}.issubset(event)


def test_compose_declares_the_end_to_end_platform():
    compose = yaml.safe_load((ROOT / "docker-compose/docker-compose.yml").read_text(encoding="utf-8"))
    services = set(compose["services"])
    assert {"spark-master", "kafka", "minio", "sqlserver", "airflow-scheduler"}.issubset(services)


def test_dags_map_to_spark_jobs():
    pairs = {
        "pmd_batch_snapshot_spark.py": "pmd_batch_snapshot.py",
        "pmd_csv_batch_medallion_spark.py": "pmd_csv_batch_medallion.py",
        "pmd_streaming_updates_spark.py": "pmd_streaming_updates.py",
    }
    for dag_name, job_name in pairs.items():
        dag = ROOT / "pipelines/dags/real" / dag_name
        assert dag.exists()
        assert job_name in dag.read_text(encoding="utf-8")
        assert (ROOT / "pipelines/spark-apps" / job_name).exists()

