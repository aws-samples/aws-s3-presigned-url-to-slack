#!/usr/bin/env python3
import os
import aws_cdk as cdk

from infra.S3PresignedStack import S3PresignedStack

BUCKET_NAME = os.environ["BUCKET_NAME"]
SLACK_CHANNEL = os.environ["SLACK_CHANNEL"]
ACCOUNT = os.environ["CDK_DEFAULT_ACCOUNT"]
REGION = os.environ["CDK_DEFAULT_REGION"]

app = cdk.App()

S3PresignedStack(
    app,
    "S3PresignedStack",
    bucket_name=BUCKET_NAME,
    slack_channel=SLACK_CHANNEL,
    env=cdk.Environment(account=ACCOUNT, region=REGION)
)


app.synth()
