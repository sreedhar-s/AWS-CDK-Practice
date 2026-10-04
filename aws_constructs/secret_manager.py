from constructs import Construct
from aws_cdk import (
    aws_secretsmanager as secretsmanager,
    CfnTag,
)
from typing import Optional, Dict

class SecretManagerConstruct(Construct):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        secret_name: str,
        username: str,
        tags: Optional[Dict[str, str]] = None,
        **kwargs,
    ) -> None:
        
        super().__init__(
            scope,
            construct_id,
            **kwargs,
        )

        self.secret = secretsmanager.CfnSecret(
            self,
            "Secret",
            name=secret_name,
            generate_secret_string=(
                secretsmanager.CfnSecret.GenerateSecretStringProperty(
                    secret_string_template=(
                        f'{{"username":"{username}"}}'
                    ),
                    generate_string_key="password",
                    password_length=32,
                    exclude_punctuation=True,
                )
            ),
            tags=[
                CfnTag(
                    key=key,
                    value=value,
                )
                for key, value in (tags or {}).items()
            ],
        )