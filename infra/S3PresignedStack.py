from aws_cdk import (
    core as cdk,
    aws_s3 as s3,
    aws_s3_notifications as s3n,
    aws_lambda as lambda_,
    aws_iam as iam,
)


class S3PresignedStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str,
                 bucket_name: str, slack_channel: str,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        lambda_role = iam.Role(
            self,
            "S3PresignedRole",
            role_name="S3PresignedRole",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess"),
                iam.ManagedPolicy.from_aws_managed_policy_name("CloudWatchLogsFullAccess"),
            ]
        )

        lambda_func = lambda_.Function(
            self,
            "PresignedLambda",
            function_name="S3PresignedGenerator",
            handler="lambda_handler.handler",
            runtime=lambda_.Runtime.PYTHON_3_9,
            code=lambda_.Code.from_asset("lambdas"),
            role=lambda_role,
            timeout=cdk.Duration.seconds(10),
            tracing=lambda_.Tracing.ACTIVE,
            insights_version=lambda_.LambdaInsightsVersion.VERSION_1_0_98_0,
        )

        lambda_func.add_environment(
            key="SLACK_CHANNEL",
            value=slack_channel
        )

        sharing_bucket = s3.Bucket(
            self,
            "SharingBucket",
            bucket_name=bucket_name
        )

        sharing_bucket.add_event_notification(
            s3.EventType.OBJECT_CREATED,
            s3n.LambdaDestination(lambda_func)
        )


