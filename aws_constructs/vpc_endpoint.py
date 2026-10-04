from constructs import Construct
from aws_cdk import (aws_ec2 as ec2, CfnTag)
from typing import Dict, Optional

class VpcEndpointConstruct(Construct):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        *,
        vpc_id: Optional[str] = None,
        private_subnet_1: Optional[str] = None,
        private_subnet_2: Optional[str] = None,
        endpoint_security_group_id: Optional[str] = None,
        route_table_ids: Optional[str] = None,
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
            route_table_ids=route_table_ids,
            tags=[
                CfnTag(
                    key=key,
                    value=value,
                )
                for key, value in (tags or {}).items()
            ]
        )