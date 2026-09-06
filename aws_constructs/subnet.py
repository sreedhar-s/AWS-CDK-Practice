from typing import Dict, Optional
from aws_cdk import ( aws_ec2 as ec2, CfnTag)
from constructs import Construct

class SubnetConstruct(Construct):
    def __init__( 
            self, 
            scope: Construct, 
            construct_id: str, *, 
            vpc: ec2.CfnVPC,
            snt_cidr: str, 
            availability_zone: str,
            tags: Optional[Dict[str, str]] = None 
        ) -> None:

        super().__init__(scope, construct_id)

        snt_tags = []

        if tags:
            snt_tags.extend(
                CfnTag(
                    key=key,
                    value=value,
                )
                for key, value in tags.items()
            )

        self.subnet = ec2.CfnSubnet( 
            self, 
            "subnet", 
            cidr_block=snt_cidr,
            vpc_id = vpc.ref,
            availability_zone = availability_zone,
            tags= snt_tags
        )