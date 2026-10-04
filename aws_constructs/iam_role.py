from constructs import Construct
from aws_cdk import (
    aws_iam as iam,
    CfnTag,
)
from typing import Optional, Dict, List


class IamRoleConstruct(Construct):

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        role_name: str,
        service_principal: str,
        managed_policy_arns: Optional[List[str]] = None,
        tags: Optional[Dict[str, str]] = None,
        **kwargs,
    ) -> None:

        super().__init__(scope, construct_id, **kwargs)

        assume_role_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {
                        "Service": service_principal,
                    },
                    "Action": "sts:AssumeRole",
                }
            ],
        }

        self.role = iam.CfnRole(
            self,
            "IamRole",
            role_name=role_name,
            assume_role_policy_document=assume_role_policy,
            managed_policy_arns=managed_policy_arns or [],
            tags=[
                CfnTag(
                    key=key,
                    value=value,
                )
                for key, value in (tags or {}).items()
            ],
        )