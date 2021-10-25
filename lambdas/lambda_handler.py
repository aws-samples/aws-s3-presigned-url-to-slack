import os
import boto3
import json
import urllib.request
import urllib.parse
import traceback


SLACK_CHANNEL = os.environ["SLACK_CHANNEL"]

client = boto3.client("s3")


def post_to_slack(message):
    body = {
        "Content": message
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
        expiration = 3600 * 24

        print(bucket_name, object_name, expiration)

        response = client.generate_presigned_url(
            "get_object",
            Params={
                "Bucket": bucket_name,
                "Key": object_name
            },
            ExpiresIn=expiration
        )

        post_to_slack(response)


def handler(event, context):
    try:
        main(event)
    except Exception as e:
        trace_str = traceback.format_exc()
        post_to_slack(trace_str)
        print(trace_str)
