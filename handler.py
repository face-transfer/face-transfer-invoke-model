from __future__ import print_function
import json
import os
import uuid
import boto3
from titus.genpy import PFAEngine

print('Creating Scoring Engine')


def download_model(bucket, key):
    download_path = f"/tmp/{uuid.uuid4()}{key}"
    s3_client = boto3.client('s3')
    s3_client.download_file(bucket, key, download_path)
    return download_path


def call(event, context):

    key = os.environ["KEY"]
    bucket = os.environ["BUCKET"]
    region = os.environ["AWS_REGION"]

    download_path = download_model(bucket, key)
    engine, = PFAEngine.fromJson(json.load(open(download_path)))
    result  = engine.action(2.5)
    # result = engine.action(event)
    response = {
        "statusCode": 301,
        "body": "",
        "headers": {
            "location": f"{download_path} ==> {result}"
        }
    }

    return response
