from constructs import Construct
from aws_cdk import (
    Stack,
    Aws,
    aws_ec2 as ec2,
    aws_eks as eks,
    CfnTag
)
from typing import Optional, Dict

class EKSClusterConstruct(Stack):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        *,
        private_subnet_1: str,
        private_subnet_2: str,
        cluster_name: str = "ue1dsatseksdv01",
        cluster_role_arn: str,
        cluster_security_group_id: str,
        node_security_group_id: str,
        node_group_name: str = "ue1dsatseksdv01-nodegroup",
        node_role_arn:str,
        kubernetes_version: str = "1.35",
        node_instance_type: str = "m7i.large",
        desired_size: int,
        min_size: int,
        max_size: int,
        tags: Optional[Dict[str, str]] = None,
        **kwargs,
    ) -> None:

        super().__init__(
            scope,
            construct_id,
            **kwargs,
        )

        self.cluster = eks.CfnCluster(
            self,
            "EKSCluster",
            name=cluster_name,
            version=kubernetes_version,
            role_arn=cluster_role_arn,
            resources_vpc_config=eks.CfnCluster.ResourcesVpcConfigProperty(
                subnet_ids=[
                    private_subnet_1,
                    private_subnet_2,
                ],
                security_group_ids=[cluster_security_group_id],
                endpoint_private_access=True,
                endpoint_public_access=False,
            ),

            access_config=eks.CfnCluster.AccessConfigProperty(
                authentication_mode="API_AND_CONFIG_MAP",
                bootstrap_cluster_creator_admin_permissions=True,
            ),

            logging=eks.CfnCluster.LoggingProperty(
                cluster_logging=eks.CfnCluster.ClusterLoggingProperty(
                    enabled_types=[
                        eks.CfnCluster.LoggingTypeConfigProperty(
                            type="api"
                        ),
                        eks.CfnCluster.LoggingTypeConfigProperty(
                            type="authenticator"
                        ),
                    ]
                )
            ),

            tags=[
                CfnTag(
                    key=key,
                    value=value,
                )
                for key, value in (tags or {}).items()
            ]
        )
        
        
        # =========================================================
        # LAUNCH TEMPLATE
        # =========================================================

        self.launch_template = ec2.CfnLaunchTemplate(
            self,
            "NodeLaunchTemplate",
            launch_template_name=f"{cluster_name}-node-lt",
            launch_template_data=ec2.CfnLaunchTemplate.LaunchTemplateDataProperty(
                block_device_mappings=[
                    ec2.CfnLaunchTemplate.BlockDeviceMappingProperty(
                        device_name="/dev/xvda",
                        ebs=ec2.CfnLaunchTemplate.EbsProperty(
                            volume_size=100,
                            volume_type="gp3",
                            encrypted=True,
                            kms_key_id="alias/aws/ebs",
                        ),
                    )
                ],
                security_group_ids=[
                    node_security_group_id
                ]
            )
        )

        # =========================================================
        # NODE GROUP
        # =========================================================

        self.node_group = eks.CfnNodegroup(
            self,
            "NodeGroup",
            cluster_name=self.cluster.ref,
            nodegroup_name=node_group_name,
            node_role=node_role_arn,
            
            ami_type="AL2023_x86_64_STANDARD",
            instance_types=[
                node_instance_type,
            ],
            launch_template=eks.CfnNodegroup.LaunchTemplateSpecificationProperty(
                id=self.launch_template.ref,
                version=self.launch_template.attr_latest_version_number,
            ),

            scaling_config=eks.CfnNodegroup.ScalingConfigProperty(
                desired_size=desired_size,
                min_size=min_size,
                max_size=max_size,
            ),

            subnets=[
                private_subnet_1,
                private_subnet_2,
            ],
        )

        # =========================================================
        # DEPENDENCIES
        # =========================================================

        self.node_group.add_dependency(self.cluster)

        # =========================================================
        # EKS ADD-ONS
        # =========================================================

        self.pod_identity_addon = eks.CfnAddon(
            self,
            "PodIdentityAgentAddon",
            cluster_name=self.cluster.ref,
            addon_name="eks-pod-identity-agent",
            resolve_conflicts="OVERWRITE",
        )

        self.vpc_cni_addon = eks.CfnAddon(
            self,
            "VpcCniAddon",
            cluster_name=self.cluster.ref,
            addon_name="vpc-cni",
            resolve_conflicts="OVERWRITE",
            configuration_values="""{
                "env": {
                    "WARM_IP_TARGET": "2",
                    "MINIMUM_IP_TARGET": "3"
                }
            }""",
        )

        self.kube_proxy_addon = eks.CfnAddon(
            self,
            "KubeProxyAddon",
            cluster_name=self.cluster.ref,
            addon_name="kube-proxy",
            resolve_conflicts="OVERWRITE",
        )

        self.coredns_addon = eks.CfnAddon(
            self,
            "CoreDnsAddon",
            cluster_name=self.cluster.ref,
            addon_name="coredns",
            resolve_conflicts="OVERWRITE",
        )

        # Add-on dependencies
        self.pod_identity_addon.add_dependency(
            self.node_group
        )

        self.vpc_cni_addon.add_dependency(
            self.node_group
        )

        self.kube_proxy_addon.add_dependency(
            self.node_group
        )

        self.coredns_addon.add_dependency(
            self.node_group
        )