from typing import Dict, Optional 
from aws_cdk import ( aws_ec2 as ec2, CfnTag) 
from constructs import Construct

class NatGatewayConstruct(Construct): 
    def __init__( 
            self, 
            scope: Construct, 
            construct_id: str, *, 
            public_subnet: ec2.CfnSubnet,
            EIP_tags: Optional[Dict[str, str]] = None, 
            Natgateway_tags: Optional[Dict[str, str]] = None, 
        ) -> None: 
        super().__init__(scope, construct_id)

        EIP_tags = []
        
        if EIP_tags:
            EIP_tags.extend(
                CfnTag(
                    key=key,
                    value=value,
                )
                for key, value in EIP_tags.items()
            )

        Natgateway_tags = []

        if Natgateway_tags:
            Natgateway_tags.extend(
                CfnTag(
                    key=key,
                    value=value,
                )
                for key, value in Natgateway_tags.items()
            )

        self.eip = ec2.CfnEIP( 
            self, 
            "NatEIP", 
            domain="vpc", 
            tags=EIP_tags, 
        )

        self.nat_gateway = ec2.CfnNatGateway( 
            self, 
            "NatGateway", 
            subnet_id=public_subnet.ref, 
            allocation_id=self.eip.attr_allocation_id, 
            connectivity_type="public", 
            tags = Natgateway_tags
        )

