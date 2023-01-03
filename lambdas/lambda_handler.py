import os
import boto3
import json
import urllib.request
import urllib.parse
import traceback

from botocore.config import Config


SLACK_CHANNEL = os.environ["SLACK_CHANNEL"]
EXPIRES_IN = os.environ["EXPIRES_IN"]

conf = Config(
    signature_version="s3v4",
    s3={"addressing_style": "path"}
)

client = boto3.client("s3", config=conf)


def post_to_slack(message):
    body = {
        "content": message
    }

    data = json.dumps(body).encode("utf8")

    req = urllib.request.Request(
        SLACK_CHANNEL,
        data=data,
        headers={"Content-Type": "application/json"}
    )

    urllib.request.urlopen(req)


def main(event):
    for record in event["Records"]:
        bucket_name = record["s3"]["bucket"]["name"]
        object_name = urllib.parse.unquote_plus(record["s3"]["object"]["key"])

        print(bucket_name, object_name, EXPIRES_IN)

        response = client.generate_presigned_url(
            ClientMethod="get_object",
            Params={
                "Bucket": bucket_name,
                "Key": object_name
            },
            HttpMethod="GET",
            ExpiresIn=int(EXPIRES_IN)
        )

        post_to_slack(response)


def handler(event, context):
    try:
        main(event)
    except Exception as e:
        trace_str = traceback.format_exc()
        post_to_slack(trace_str)
        print(trace_str)
