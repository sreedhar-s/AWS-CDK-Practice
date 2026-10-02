from constructs import Construct
from aws_cdk import aws_organizations as organizations

class OrganizationalUnitConstruct(Construct):

    def __init__(
        self, 
        scope: Construct, 
        construct_id: str, *, 
        parent_id: str,
        ou_name: str,
        ) -> None:
        
        super().__init__(scope, construct_id)

        self.ou = organizations.CfnOrganizationalUnit(
            self,
            "OrganizationalUnit",
            name=ou_name,
            parent_id=parent_id,
        )