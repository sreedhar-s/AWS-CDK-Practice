from typing import Dict, List, Optional 
from aws_cdk import ( aws_ec2 as ec2, CfnTag) 
from constructs import Construct

class TgwRouteTableConstrcut(Construct):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        transit_gateway_id: str,
        
        tags: Optional[Dict[str, str]] = None,  
    ) -> None:
        super().__init__(scope, construct_id)

        tgw_rtb_tags = []
                    
        if tags:
            tgw_rtb_tags.extend(
                CfnTag(
                    key=key,
                    value=value,
                )
                for key, value in tags.items()
            )

        tgw_route_table = ec2.CfnTransitGatewayRouteTable(
            self,
            "TgwRouteTable",
            transit_gateway_id=transit_gateway_id,
            tags = tgw_rtb_tags
        )