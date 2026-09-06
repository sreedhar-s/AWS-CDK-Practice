from typing import Dict, List, Optional 
from aws_cdk import ( aws_ec2 as ec2, CfnTag) 
from constructs import Construct

class TransitGatewayAttachmentConstruct(Construct): 
    def __init__( 
        self, 
        scope: Construct, 
        construct_id: str, *, 
        transit_gateway_id: str, 
        vpc_id: str, 
        subnet_ids: List[str],
        tags: Optional[Dict[str, str]] = None,
    ) -> None: 
        super().__init__(scope, construct_id)

        tgw_att_tags = []
                    
        if tags:
            tgw_att_tags.extend(
                CfnTag(
                    key=key,
                    value=value,
                )
                for key, value in tags.items()
            )

        self.attachment = ec2.CfnTransitGatewayAttachment( 
            self, 
            "TransitGatewayVpcAttachment", 
            transit_gateway_id=transit_gateway_id,
            vpc_id=vpc_id, 
            subnet_ids=subnet_ids, 
            tags=tgw_att_tags
        )
