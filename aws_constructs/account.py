from constructs import Construct
from aws_cdk import aws_organizations as organizations

class AccountConstruct(Construct):
    def __init__(
            self, 
            scope: Construct, 
            construct_id: str, *, 
            account_name: str,
            email: str,
            ou_id: str,
            **kwargs,
        ) -> None:
        
        super().__init__(scope, construct_id, **kwargs)

        self.account = organizations.CfnAccount(
            self,
            "Account",
            account_name=account_name,
            email=email,
            parent_ids=[ou_id],
        )