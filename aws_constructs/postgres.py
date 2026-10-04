from constructs import Construct
from aws_cdk import (
    aws_rds as rds,
    CfnTag,
)
from typing import Optional, Dict


class PostgresRDSConstruct(Construct):

    def __init__(
        self,
        scope: Construct,
        construct_id: str,

        # Database
        db_name: str,
        master_username: str,
        master_password: str,
        db_identifier: str,

        # Networking
        subnet_ids: list[str],
        security_group_id: str,

        # IAM
        monitoring_role_arn: str,

        # Tags
        tags: Optional[Dict[str, str]] = None,

        **kwargs,
    ) -> None:

        super().__init__(
            scope,
            construct_id,
            **kwargs,
        )

        # --------------------------------------------------
        # DB Subnet Group
        # --------------------------------------------------

        self.subnet_group = rds.CfnDBSubnetGroup(
            self,
            "PostgresSubnetGroup",

            db_subnet_group_description=(
                "Subnet group for PostgreSQL RDS"
            ),

            subnet_ids=subnet_ids,

            tags=[
                CfnTag(
                    key=key,
                    value=value,
                )
                for key, value in (tags or {}).items()
            ],
        )

        # --------------------------------------------------
        # PostgreSQL RDS
        # --------------------------------------------------

        self.database = rds.CfnDBInstance(
            self,
            "PostgresRDS",
            db_instance_identifier=db_identifier,
            engine="postgres",
            engine_version="18.6-R1",
            # RDS Extended Support
            engine_lifecycle_support=(
                "open-source-rds-extended-support"
            ),
            db_instance_class="db.m7g.large",
            storage_type="gp3",
            allocated_storage="50",
            db_name=db_name,
            master_username=master_username,
            master_user_password=master_password,
            enable_iam_database_authentication=False,
            multi_az=False,
            db_subnet_group_name=self.subnet_group.ref,
            vpc_security_groups=[
                security_group_id,
            ],
            publicly_accessible=False,
            database_insights_mode="standard",
            monitoring_interval=60,
            monitoring_role_arn=monitoring_role_arn,
            backup_retention_period=30,
            deletion_protection=True,
            copy_tags_to_snapshot=True,
            tags=[
                CfnTag(
                    key=key,
                    value=value,
                )
                for key, value in (tags or {}).items()
            ],
        )
        
        self.database.add_dependency(
            self.subnet_group
        )