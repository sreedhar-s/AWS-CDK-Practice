from typing import Dict, Optional 
from aws_cdk import ( aws_ec2 as ec2, CfnTag) 
from constructs import Construct

class InternetGatewayConstruct(Construct): 
    def __init__( 
            self, 
            scope: Construct, 
            construct_id: str, *, 
            vpc: ec2.CfnVPC, 
            tags: Optional[Dict[str, str]] = None, 
        ) -> None:

        super().__init__(scope, construct_id)

        igw_tags = []
        
        if tags:
            igw_tags.extend(
                CfnTag(
                    key=key,
                    value=value,
                )
                for key, value in tags.items()
            )

        self.internet_gateway = ec2.CfnInternetGateway( 
            self, 
            "InternetGateway", 
            tags= igw_tags 
        )

        self.attachment = ec2.CfnVPCGatewayAttachment( 
            self, 
            "InternetGatewayAttachment", 
            vpc_id=vpc.ref, 
            internet_gateway_id=self.internet_gateway.ref, 
        )


