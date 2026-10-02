from aws_cdk import Stack 
from constructs import Construct

from aws_constructs.org_unit import OrganizationalUnitConstruct
from aws_constructs.account import AccountConstruct

class ManagementStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        security = OrganizationalUnitConstruct(
            self,
            "test OU",
            parent_id="r-1ofw",
            ou_name="test OU",
        )
        
        # test_acc = AccountConstruct(
        #     self,
        #     "test-acc",
        #     account_name="test-acc",
        #     email="test-acc@mindsprint.com",
        #     ou_id="ou-1ofw-6mx6lk9l"
        # )

