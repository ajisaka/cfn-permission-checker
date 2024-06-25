from typing import Any

import boto3

from app.cache import Cache

_cfn = boto3.client("cloudformation")
_s3 = boto3.client("s3")


# @Cache
def fetch_log_files(bucket_name: str) -> list[Any]:  # list[s3_object_summary]
    result = []

    paginator = _s3.get_paginator("list_objects_v2")
    for page in paginator.paginate(Bucket=bucket_name):
        for obj in page["Contents"]:
            key = obj["Key"]
            if key.endswith(".json.gz"):
                result.append(obj)

    return result


@Cache
def fetch_stack(stack_name: str = "cfn-api-tracer") -> Any:
    return _cfn.describe_stacks(StackName=stack_name)["Stacks"][0]


@Cache
def fetch_s3_bytes(bucket_name: str, key: str) -> Any:
    return _s3.get_object(Bucket=bucket_name, Key=key)["Body"].read()
