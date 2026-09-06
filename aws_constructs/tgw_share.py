from typing import Dict, Optional 
from aws_cdk import (aws_ram as ram, CfnTag)
from constructs import Construct

class TransitGatewayShareConstruct(Construct): 
    def __init__( 
        self, 
        scope: Construct, 
        construct_id: str, *, 
        transit_gateway_arn: str, 
        target_account_id: str, 
        share_name: str, 
        allow_external_principals: bool = True, 
        tags: Optional[Dict[str, str]] = None, 
    ) -> None: 
        super().__init__(scope, construct_id) 
        
        share_tags = []

        if tags:
            share_tags.extend(
                CfnTag(
                    key=key,
                    value=value,
                )
                for key, value in tags.items()
            )

        self.resource_share = ram.CfnResourceShare( 
            self, 
            "TransitGatewayResourceShare", 
            name=share_name,
            resource_arns=[ transit_gateway_arn ],  
            principals=[ target_account_id ], 
            allow_external_principals=allow_external_principals,
            tags = share_tags
        )
