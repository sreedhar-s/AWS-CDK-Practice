from typing import Dict, Optional
from aws_cdk import ( aws_ec2 as ec2, CfnTag)
from constructs import Construct

class RoutetableConstruct(Construct):
    def __init__( 
            self, 
            scope: Construct, 
            construct_id: str, *, 
            vpc: ec2.CfnVPC,
            tags: Optional[Dict[str, str]] = None 
        ) -> None:

        super().__init__(scope, construct_id)

        rtb_tags = []

        if tags:
            rtb_tags.extend(
                CfnTag(
                    key=key,
                    value=value,
                )
                for key, value in tags.items()
            )

        self.route_table = ec2.CfnRouteTable( 
            self, 
            "route_table", 
            vpc_id = vpc.ref,
            tags= rtb_tags
        )