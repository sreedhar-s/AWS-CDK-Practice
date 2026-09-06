from typing import Dict, List, Optional 
from aws_cdk import ( aws_ec2 as ec2, CfnTag) 
from constructs import Construct

class TransitGatewayConstruct(Construct):
    def __init__( 
            self, 
            scope: Construct, 
            construct_id: str, *, 
            transit_gateway_cidr_blocks: Optional[List[str]] = None, 
            tags: Optional[Dict[str, str]] = None, 
        ) -> None: 

            super().__init__(scope, construct_id)

            tgw_tags = []
            
            if tags:
                tgw_tags.extend(
                    CfnTag(
                        key=key,
                        value=value,
                    )
                    for key, value in tags.items()
                )

            self.transit_gateway = ec2.CfnTransitGateway( 
                self, 
                "TransitGateway", 
                dns_support="enable", 
                vpn_ecmp_support="enable", 
                default_route_table_association="enable", 
                default_route_table_propagation="enable",
                auto_accept_shared_attachments = "enable",
                tags = tgw_tags
            )