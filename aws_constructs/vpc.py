from typing import Dict, Optional
from aws_cdk import ( aws_ec2 as ec2, CfnTag)
from constructs import Construct

class VpcConstruct(Construct):
    def __init__( 
            self, 
            scope: Construct, 
            construct_id: str, *, 
            vpc_cidr: str, 
            tags: Optional[Dict[str, str]] = None 
        ) -> None:

        super().__init__(scope, construct_id)

        vpc_tags = []

        if tags:
            vpc_tags.extend(
                CfnTag(
                    key=key,
                    value=value,
                )
                for key, value in tags.items()
            )

        self.vpc = ec2.CfnVPC( 
            self, 
            "Vpc", 
            cidr_block=vpc_cidr, 
            enable_dns_support=True, 
            enable_dns_hostnames=True, 
            tags= vpc_tags
        )