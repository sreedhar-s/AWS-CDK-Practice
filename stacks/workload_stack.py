from aws_cdk import Stack 
from constructs import Construct

from aws_constructs.vpc import VpcConstruct
from aws_constructs.subnet import SubnetConstruct
from aws_constructs.s3 import S3BucketConstruct
from aws_constructs.security_group import SecurityGroupConstruct
from aws_constructs.postgres import PostgresRDSConstruct
from aws_constructs.iam_role import IamRoleConstruct

class WorkloadStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        demo_vpc = VpcConstruct(
            self,
            "demo_vpc",
            vpc_cidr ="10.42.58.0/24",
            tags={
                "Name": "demo-vpc"
            }
        )

        demo_pvt_snt_1a = SubnetConstruct(
            self,
            "demo_pvt_snt_1a",
            vpc = demo_vpc.vpc,
            snt_cidr = "10.42.58.0/28",
            availability_zone = "ap-southeast-1a",
            tags = {
                "Name": "demo_pvt_snt_1a"
            }
        )

        demo_pvt_snt_1b = SubnetConstruct(
            self,
            "demo_pvt_snt_1b",
            vpc=demo_vpc.vpc,
            snt_cidr="10.42.58.16/28",
            availability_zone="ap-southeast-1b",
            tags={
                "Name": "demo_pvt_snt_1b"
            }
        )
        
        demo_s3 = S3BucketConstruct(
            self,
            "ue1-demo-cloudtrail-pr",
            bucket_name="ue1-demo-cloudtrail-pr",
            tags = {
                "Name": "ue1-demo-cloudtrail-pr"
            }
        )
        
        postgres_sg = SecurityGroupConstruct(
            self,
            "PostgresSecurityGroup",
            vpc_id=demo_vpc.vpc.ref,
            description=(
                "Security group for PostgreSQL RDS"
            ),

            ingress_rules=[
                {
                    "protocol": "tcp",
                    "from_port": 5432,
                    "to_port": 5432,
                    "cidr_ip": "10.0.0.0/8",
                    "description": (
                        "PostgreSQL access from internal network"
                    ),
                }
            ],

            tags={
                "Name": "postgres-sg",
                "Environment": "dev",
            },
        )
        
        rds_monitoring_role = IamRoleConstruct(
            self,
            "RDSMonitoringRole",
            role_name="rds-enhanced-monitoring-role",
            service_principal=(
                "monitoring.rds.amazonaws.com"
            ),
            managed_policy_arns=[
                (
                    "arn:aws:iam::aws:policy/"
                    "service-role/"
                    "AmazonRDSEnhancedMonitoringRole"
                )
            ],

            tags={
                "Name": "rds-monitoring-role",
                "Environment": "dev",
            },
        )
        
        postgres = PostgresRDSConstruct(
            self,
            "PostgresRDS",
            db_name="demodb",
            engine="postgres",
            engine_version="18.4",
            master_username="postgres",
            
            db_identifier="demo-postgres",
            subnet_ids=[
                demo_pvt_snt_1a.subnet.ref,
                demo_pvt_snt_1b.subnet.ref
            ],

            security_group_id=(
                postgres_sg.security_group.attr_group_id
            ),

            monitoring_role_arn=(
                rds_monitoring_role.role.attr_arn
            ),

            tags={
                "Name": "demo-postgres",
                "Environment": "dev",
                "Project": "demo"
            },
        )
        
        
        
        
        









        

        
















