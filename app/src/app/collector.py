import json
import sys
from pathlib import Path
from typing import Any, Iterator

import app.aws as aws
from app.filter import Filter
from app.paths import UserDataDirectory


def collect_records(filter: Filter) -> Iterator[Any]:
    bucket_name = _fetch_bucket_name()

    for record in _iter_records(bucket_name, filter):
        yield record


def _iter_records(bucket_name: str, filter: Filter) -> Iterator[Any]:
    bucket_name = _fetch_bucket_name()

    print(f"!! List log files", file=sys.stderr)

    objects = aws.fetch_log_files(bucket_name)

    print(f"!! Fetch log file contents", file=sys.stderr)

    for obj in objects:
        if not filter.match_s3_object(obj):
            continue
        records = _fetch_records(bucket_name, obj["Key"])
        for record in records:
            if not filter.match(record):
                continue
            if record["userAgent"] == "cloudformation.amazonaws.com":
                yield record


def _fetch_bucket_name() -> str:
    bucket_name: None | str = None

    for pair in aws.fetch_stack()["Outputs"]:
        if pair["OutputKey"] == "BucketName":
            bucket_name = pair["OutputValue"]
            break
    assert bucket_name is not None

    return bucket_name


def _extract_gz(content: bytes) -> bytes:
    import gzip
    import io

    with gzip.GzipFile(fileobj=io.BytesIO(content)) as f:
        return f.read()


def _fetch_records(bucket_name: str, key: str) -> Any:
    file_path = _record_cache_filepath(key)

    if file_path.exists():
        with open(file_path) as f:
            return json.load(f)

    body = aws.fetch_s3_bytes(bucket_name=bucket_name, key=key)
    records = json.loads(_extract_gz(body))["Records"]

    file_path.parent.mkdir(parents=True, exist_ok=True)

    with open(file_path, "w") as f:
        json.dump(records, f, indent=2)

    return records


def _record_cache_filepath(key: str) -> Path:
    return UserDataDirectory / f"""records/{key.removesuffix(".gz")}"""
