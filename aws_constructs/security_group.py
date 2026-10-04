from constructs import Construct
from aws_cdk import (
    aws_ec2 as ec2,
    CfnTag,
)
from typing import Optional, Dict, List


class SecurityGroupConstruct(Construct):

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        vpc_id: str,
        description: str,
        group_name: str,
        tags: Optional[Dict[str, str]] = None,
        **kwargs,
    ) -> None:

        super().__init__(scope, construct_id, **kwargs)
        
        sg_tags = []
        
        if tags:
            sg_tags.extend(
                CfnTag(
                    key=key,
                    value=value,
                )
                for key, value in tags.items()
            )
      
        self.security_group = ec2.CfnSecurityGroup(
            self,
            "SecurityGroup",
            group_name=group_name,
            group_description=description,
            vpc_id=vpc_id,
            tags=sg_tags
        )