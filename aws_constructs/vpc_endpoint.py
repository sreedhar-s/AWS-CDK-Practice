from constructs import Construct
from aws_cdk import (aws_ec2 as ec2, CfnTag)
from typing import Dict, Optional

class VpcEndpointConstruct(Construct):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        *,
        vpc_id: str,
        private_subnet_1: str,
        private_subnet_2: str,
        endpoint_security_group_id: str,
        service_name: str,
        vpc_endpoint_type: str,
        tags: Optional[Dict[str, str]] = None,
    ) -> None:
        super().__init__(scope, construct_id)

        subnet_ids = [
            private_subnet_1,
            private_subnet_2,
        ]

        security_group_ids = [
            endpoint_security_group_id,
        ]

        self.vpc_endpoint = ec2.CfnVPCEndpoint(
            self,
            "VpcEndpoint",
            vpc_id=vpc_id,
            service_name=service_name,
            vpc_endpoint_type=vpc_endpoint_type,
            private_dns_enabled=True,
            subnet_ids=subnet_ids,
            security_group_ids=security_group_ids,
            tags=[
                CfnTag(
                    key=key,
                    value=value,
                )
                for key, value in (tags or {}).items()
            ]
        )