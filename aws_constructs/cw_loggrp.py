from aws_cdk import ( aws_logs as logs )
from constructs import Construct

class CloudWatchLogGroup(Construct):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        log_group_name: str,
        retention: int,
    ) -> None:
        super().__init__(scope, construct_id)

        self.log_group = logs.CfnLogGroup(
            self,
            "LogGroup",
            log_group_name=log_group_name,
            retention_in_days=retention
        )