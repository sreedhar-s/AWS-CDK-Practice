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
        ingress_rules: Optional[List[Dict]] = None,
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
            group_description=description,
            vpc_id=vpc_id,
            tags=sg_tags
        )

        # -----------------------------------------
        # Ingress Rules
        # -----------------------------------------

        for index, rule in enumerate(ingress_rules or []):

            ec2.CfnSecurityGroupIngress(
                self,
                f"IngressRule{index}",
                group_id=self.security_group.attr_group_id,
                ip_protocol=rule.get("protocol", "tcp"),
                from_port=rule.get("from_port"),
                to_port=rule.get("to_port"),
                cidr_ip=rule.get("cidr_ip"),
                description=rule.get("description"),
            )