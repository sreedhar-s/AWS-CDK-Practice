from aws_cdk import aws_ec2 as ec2
from constructs import Construct
from typing import List, Dict, Optional
 
class SecurityGroupIngressConstruct(Construct):
    def __init__(
            self,
            scope: Construct,
            construct_id: str,
            ingress_rules: Optional[List[Dict]] = None,
            **kwargs,
        ) -> None:
    
            super().__init__(scope, construct_id, **kwargs)
    
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
                    source_security_group_id=rule.get("source_security_group_id")
                )