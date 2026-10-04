from aws_cdk import Stack 
from constructs import Construct

from aws_constructs.vpc import VpcConstruct
from aws_constructs.subnet import SubnetConstruct
from aws_constructs.security_group import SecurityGroupConstruct
from aws_constructs.iam_role import IamRoleConstruct
from aws_constructs.vpc_endpoint import VpcEndpointConstruct
from aws_constructs.sg_ingress_rules import SecurityGroupIngressConstruct
from aws_constructs.eks import EKSClusterConstruct

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
        
        cluster_sg = SecurityGroupConstruct(
            self,
            "ClusterSecurityGroup",
            vpc_id=demo_vpc.vpc.ref,
            group_name="cluster-sg",
            description=(
                "Security group for EKS Cluster"
            ),
            tags={
                "Name": "cluster-sg"
            }
        )
        
        node_sg = SecurityGroupConstruct(
            self,
            "NodeSecurityGroup",
            vpc_id=demo_vpc.vpc.ref,
            group_name="node-sg",
            description=(
                "Security group for EKS Nodes"
            ),

            tags={
                "Name": "node-sg"
            }
        )
        
        vpcendpoint_sg = SecurityGroupConstruct(
            self,
            "VPCEnpointSecurityGroup",
            vpc_id=demo_vpc.vpc.ref,
            group_name = "vpc-endpoint-sg",
            description=(
                "Security group for VPC Enpoints"
            ),
            tags={
                "Name": "vpc-endpoint-sg"
            }
        )
        
        # =========================================================
        # External to Cluster 80 and 443 Ingress Rules
        # =========================================================
        
        ClusterIngress80 = SecurityGroupIngressConstruct(
            self,
            "ClusterIngress80",
            group_id=cluster_sg.security_group.ref,
            ingress_rules = [
                {
                    "ip_protocol": "tcp",
                    "from_port": 80,
                    "to_port": 80,
                    "cidr_ip": "10.0.0.0/8"
                },
                
            ]
        )
        
        ClusterIngress443 = SecurityGroupIngressConstruct(
            self,
            "ClusterIngress443",
            group_id=cluster_sg.security_group.ref,
            ingress_rules=[
                {
                    "ip_protocol": "tcp",
                    "from_port": 443,
                    "to_port": 443,
                    "cidr_ip": "10.0.0.0/8"
                }
            ]
        )
        
        # =========================================================
        # External to Nodes 80 and 443 Ingress Rules
        # =========================================================
        
        NodeIngress80 = SecurityGroupIngressConstruct(
            self,
            "NodeIngress80",
            group_id=node_sg.security_group.ref,
            ingress_rules=[
                {
                    "ip_protocol": "tcp",
                    "from_port": 80,
                    "to_port": 80,
                    "cidr_ip": "10.0.0.0/8"
                }
            ]
        )
        
        NodeIngress443 = SecurityGroupIngressConstruct(
            self,
            "NodeIngress443",
            group_id=node_sg.security_group.ref,
            ingress_rules=[
                {
                    "ip_protocol": "tcp",
                    "from_port": 443,
                    "to_port": 443,
                    "cidr_ip": "10.0.0.0/8"
                }
            ]
        )
        
        # =========================================================
        # NODE -> NODE
        # =========================================================

        NodeSelfIngress = SecurityGroupIngressConstruct(
            self,
            "NodeSelfIngress",
            group_id=node_sg.security_group.ref,
            ingress_rules=[
                {
                    "ip_protocol": "-1",
                    "source_security_group_id": node_sg.security_group.ref
                }
            ]
        )
        
        # =========================================================
        # NODE -> CLUSTER
        # =========================================================

        ClusterIngressFromNodes = SecurityGroupIngressConstruct(
            self,
            "ClusterIngressFromNodes",
            group_id=cluster_sg.security_group.ref,
            ingress_rules=[
                {
                    "ip_protocol": "tcp",
                    "from_port": 443,
                    "to_port": 443,
                    "source_security_group_id": node_sg.security_group.ref
                }
            ]
        )
        
        # =========================================================
        # CLUSTER -> NODE
        # =========================================================

        NodeIngressFromCluster = SecurityGroupIngressConstruct(
            self,
            "NodeIngressFromCluster",
            group_id=node_sg.security_group.ref,
            ingress_rules=[
                {
                    "ip_protocol": "tcp",
                    "from_port": 443,
                    "to_port": 443,
                    "source_security_group_id": cluster_sg.security_group.ref
                }
            ]
        )

        NodeIngress443FromCluster = SecurityGroupIngressConstruct(
            self,
            "NodeIngress443FromCluster",
            group_id=node_sg.security_group.ref,
            ingress_rules=[
                {
                    "ip_protocol": "tcp",
                    "from_port": 443,
                    "to_port": 443,
                    "source_security_group_id": cluster_sg.security_group.ref
                }
            ]
        )
        
        # =========================================================
        # NODE -> VPC ENDPOINTS
        # =========================================================

        VpcEndpointIngressFromNodes = SecurityGroupIngressConstruct(
            self,
            "VpcEndpointIngressFromNodes",
            group_id=vpcendpoint_sg.security_group.ref,
            ingress_rules=[
                {
                    "ip_protocol": "tcp",
                    "from_port": 443,
                    "to_port": 443,
                    "source_security_group_id": node_sg.security_group.ref
                }
            ]
        )
        
        # =========================================================
        # CLUSTER -> VPC ENDPOINTS
        # =========================================================

        VpcEndpointIngressFromCluster = SecurityGroupIngressConstruct(
            self,
            "VpcEndpointIngressFromCluster",
            group_id=vpcendpoint_sg.security_group.ref,
            ingress_rules=[
                {
                    "ip_protocol": "tcp",
                    "from_port": 443,
                    "to_port": 443,
                    "source_security_group_id": cluster_sg.security_group.ref
                }
            ]
        )
        
        # =========================================================
        # ECR API ENDPOINT
        # =========================================================

        ecr_api_endpoint = VpcEndpointConstruct(
            self,
            "EcrApiEndpoint",
            vpc_id=demo_vpc.vpc.ref,
            private_subnet_1=demo_pvt_snt_1a.subnet.ref,
            private_subnet_2=demo_pvt_snt_1b.subnet.ref,
            service_name=f"com.amazonaws.us-east-1.ecr.api",
            vpc_endpoint_type="Interface",
            
            endpoint_security_group_id=vpcendpoint_sg.security_group.ref,
            tags = {
                "Name": "ecr-api-endpoint"
            }
        )
        
        # =========================================================
        # ECR DKR ENDPOINT
        # =========================================================

        ecr_dkr_endpoint = VpcEndpointConstruct(
            self,
            "EcrDkrEndpoint",
            vpc_id=demo_vpc.vpc.ref,
            private_subnet_1=demo_pvt_snt_1a.subnet.ref,
            private_subnet_2=demo_pvt_snt_1b.subnet.ref,
            service_name=f"com.amazonaws.us-east-1.ecr.dkr",
            vpc_endpoint_type="Interface",
            
            endpoint_security_group_id=vpcendpoint_sg.security_group.ref,
            tags = {
                "Name": "ecr-dkr-endpoint"
            }
        )
        
        # =========================================================
        # STS ENDPOINT
        # =========================================================

        sts_endpoint = VpcEndpointConstruct(
            self,
            "StsEndpoint",
            vpc_id=demo_vpc.vpc.ref,
            private_subnet_1=demo_pvt_snt_1a.subnet.ref,
            private_subnet_2=demo_pvt_snt_1b.subnet.ref,
            service_name=f"com.amazonaws.us-east-1.sts",
            vpc_endpoint_type="Interface",
            endpoint_security_group_id=vpcendpoint_sg.security_group.ref,
            tags = {
                "Name": "sts-endpoint"
            }
        )
        
        # =========================================================
        # EKS ENDPOINT
        # =========================================================

        eks_endpoint = VpcEndpointConstruct(
            self,
            "EksEndpoint",
            vpc_id=demo_vpc.vpc.ref,
            private_subnet_1=demo_pvt_snt_1a.subnet.ref,
            private_subnet_2=demo_pvt_snt_1b.subnet.ref,
            service_name=f"com.amazonaws.us-east-1.eks",
            vpc_endpoint_type="Interface",
            
            endpoint_security_group_id=vpcendpoint_sg.security_group.ref,
            tags = {
                "Name": "eks-endpoint"
            }
        )
        
        # =========================================================
        # EKS AUTH ENDPOINT
        # =========================================================

        eks_auth_endpoint = VpcEndpointConstruct(
            self,
            "EksAuthEndpoint",
            vpc_id=demo_vpc.vpc.ref,
            private_subnet_1=demo_pvt_snt_1a.subnet.ref,
            private_subnet_2=demo_pvt_snt_1b.subnet.ref,
            service_name=f"com.amazonaws.us-east-1.eks-auth",
            vpc_endpoint_type="Interface",
            
            endpoint_security_group_id=vpcendpoint_sg.security_group.ref,
            tags = {
                "Name": "eks-auth-endpoint"
            }
        )
        
        # =========================================================
        # S3 ENDPOINT
        # =========================================================

        s3_endpoint = VpcEndpointConstruct(
            self,
            "S3Endpoint",
            vpc_id=demo_vpc.vpc.ref,
            private_subnet_1=demo_pvt_snt_1a.subnet.ref,
            private_subnet_2=demo_pvt_snt_1b.subnet.ref,
            service_name=f"com.amazonaws.us-east-1.s3",
            vpc_endpoint_type="Gateway",
            
            endpoint_security_group_id=vpcendpoint_sg.security_group.ref,
            tags = {
                "Name": "s3-endpoint"
            }
        )
        
        # =========================================================
        # Secret Manager ENDPOINT
        # =========================================================

        secret_manager_endpoint = VpcEndpointConstruct(
            self,
            "SecretManagerEndpoint",
            vpc_id=demo_vpc.vpc.ref,
            private_subnet_1=demo_pvt_snt_1a.subnet.ref,
            private_subnet_2=demo_pvt_snt_1b.subnet.ref,
            service_name=f"com.amazonaws.us-east-1.secretsmanager",
            vpc_endpoint_type="Gateway",
            
            endpoint_security_group_id=vpcendpoint_sg.security_group.ref,
            tags = {
                "Name": "secret-manager-endpoint"
            }
        )
        
        # =========================================================
        # EC2 ENDPOINT
        # =========================================================

        ec2_endpoint = VpcEndpointConstruct(
            self,
            "EC2Endpoint",
            vpc_id=demo_vpc.vpc.ref,
            private_subnet_1=demo_pvt_snt_1a.subnet.ref,
            private_subnet_2=demo_pvt_snt_1b.subnet.ref,
            service_name=f"com.amazonaws.us-east-1.ec2",
            vpc_endpoint_type="Gateway",
            
            endpoint_security_group_id=vpcendpoint_sg.security_group.ref,
            tags = {
                "Name": "ec2-endpoint"
            }
        )
        
        # =========================================================
        # SSM ENDPOINT
        # =========================================================

        ssm_endpoint = VpcEndpointConstruct(
            self,
            "SSMEndpoint",
            vpc_id=demo_vpc.vpc.ref,
            private_subnet_1=demo_pvt_snt_1a.subnet.ref,
            private_subnet_2=demo_pvt_snt_1b.subnet.ref,
            service_name=f"com.amazonaws.us-east-1.ssm",
            vpc_endpoint_type="Gateway",
            
            endpoint_security_group_id=vpcendpoint_sg.security_group.ref,
            tags = {
                "Name": "ssm-endpoint"
            }
        )
                
        # =========================================================
        # SSM MESSAGES ENDPOINT
        # =========================================================

        ssm_messages_endpoint = VpcEndpointConstruct(
            self,
            "SSMMessagesEndpoint",
            vpc_id=demo_vpc.vpc.ref,
            private_subnet_1=demo_pvt_snt_1a.subnet.ref,
            private_subnet_2=demo_pvt_snt_1b.subnet.ref,
            service_name=f"com.amazonaws.us-east-1.ssmmessages",
            vpc_endpoint_type="Gateway",
            
            endpoint_security_group_id=vpcendpoint_sg.security_group.ref,
            tags = {
                "Name": "ssm-messages-endpoint"
            }
        )
        
        # =========================================================
        # EKS CLUSTER IAM ROLE
        # =========================================================
        
        eks_cluster_role = IamRoleConstruct(
            self,
            "EKSClusterRole",
            role_name="eks-cluster-role",
            service_principal=(
                "eks.amazonaws.com"
            ),
            managed_policy_arns=[
                (
                    "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
                )
            ],

            tags={
                "Name": "eks-cluster-role"
            },
        )
        
        # =========================================================
        # NODE GROUP IAM ROLE
        # =========================================================
        
        eks_node_group_role = IamRoleConstruct(
            self,
            "EKSNodeGroupRole",
            role_name="eks-node-group-role",
            service_principal=(
                "eks.amazonaws.com"
            ),
            managed_policy_arns=[
                "arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy",
                "arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy",
                "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly",
                "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
            ],

            tags={
                "Name": "eks-node-group-role"
            },
        )
        
        # =========================================================
        # EKS CLUSTER
        # =========================================================
        
        demo_eks_cluster = EKSClusterConstruct(
            self,
            "DemoEksCluster",
            private_subnet_1 = demo_pvt_snt_1a.subnet.ref,
            private_subnet_2 = demo_pvt_snt_1b.subnet.ref,
            cluster_name = "demo-cluster",
            cluster_role_arn= eks_cluster_role.role.attr_arn,
            cluster_security_group_id= cluster_sg.security_group.attr_group_id,
            node_security_group_id= node_sg.security_group.attr_group_id,
            node_group_name = "demo-nodegroup",
            node_role_arn= eks_node_group_role.role.attr_arn,
            kubernetes_version = "1.36",
            node_instance_type = "m7i.large",
            desired_size=2,
            min_size= 2,
            max_size=2,
            tags = {
                "Name": "demo-cluster"
            }
        )
        
        
        
        









        

        
















