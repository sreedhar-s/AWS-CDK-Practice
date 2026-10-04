from constructs import Construct
from aws_cdk import (
    aws_s3 as s3,
    RemovalPolicy,
    Tags
)
from typing import Optional, Dict



class S3BucketConstruct(Construct):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        bucket_name: str | None = None,
        tags: Optional[Dict[str, str]] = None,
        **kwargs,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.bucket = s3.Bucket(
            self,
            "S3Bucket",
            bucket_name=bucket_name,

            # Security
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            encryption=s3.BucketEncryption.S3_MANAGED,

            # Data protection
            versioned=True,

            # Removal behavior
            removal_policy=RemovalPolicy.RETAIN
        )
        
        if tags:
            for key, value in tags.items():
                Tags.of(self.bucket).add(key, value)