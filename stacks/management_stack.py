from aws_cdk import Stack 
from constructs import Construct

from aws_constructs.org_unit import OrganizationalUnitConstruct

class ManagementStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        security = OrganizationalUnitConstruct(
            self,
            "test OU",
            parent_id="o-kpzwrqcq26",
            ou_name="test OU",
        )
