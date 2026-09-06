from aws_cdk import Stack 
from constructs import Construct

from aws_constructs.vpc import VpcConstruct
from aws_constructs.subnet import SubnetConstruct
from aws_constructs.route_table import RoutetableConstruct
from aws_constructs.route_table_snt_association import Routetable_Snt_Association_Construct
from aws_constructs.nat_gateway import NatGatewayConstruct
from aws_constructs.internet_gateway import InternetGatewayConstruct
from aws_constructs.tgw import TransitGatewayConstruct
from aws_constructs.tgw_share import TransitGatewayShareConstruct
from aws_constructs.tgw_routetable import TgwRouteTableConstrcut
from aws_constructs.aws_firewall import NetworkFirewallConstruct
from aws_constructs.firewall_policy import FirewallPolicyConstruct
from aws_constructs.cw_loggrp import CloudWatchLogGroup

class NetworkStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # demo_vpc = VpcConstruct(
        #     self,
        #     "demo_vpc",
        #     vpc_cidr ="10.42.58.0/24",
        #     tags={
        #         "Name": "demo-vpc"
        #     }
        # )

        # demo_pvt_snt_1a = SubnetConstruct(
        #     self,
        #     "demo_pvt_snt_1a",
        #     vpc = demo_vpc.vpc,
        #     snt_cidr = "10.42.58.0/28",
        #     availability_zone = "ap-southeast-1a",
        #     tags = {
        #         "Name": "demo_pvt_snt_1a"
        #     }
        # )

        # demo_pvt_snt_1b = SubnetConstruct(
        #     self,
        #     "demo_pvt_snt_1b",
        #     vpc=demo_vpc.vpc,
        #     snt_cidr="10.42.58.16/28",
        #     availability_zone="ap-southeast-1b",
        #     tags={
        #         "Name": "demo_pvt_snt_1b"
        #     }
        # )

        # demo_pub_snt_1a = SubnetConstruct(
        #     self,
        #     "demo_pub_snt_1a",
        #     vpc = demo_vpc.vpc,
        #     snt_cidr = "10.42.58.32/28",
        #     availability_zone = "ap-southeast-1a",
        #     tags = {
        #         "Name": "demo_pub_snt_1a"
        #     }
        # )

        # demo_pub_snt_1b = SubnetConstruct(
        #     self,
        #     "demo_pub_snt_1b",
        #     vpc = demo_vpc.vpc,
        #     snt_cidr = "10.42.58.48/28",
        #     availability_zone = "ap-southeast-1b",
        #     tags = {
        #         "Name": "demo_pub_snt_1b"
        #     }
        # )

        # demo_pvt_rtb = RoutetableConstruct(
        #     self,
        #     "demo_pvt_rtb",
        #     vpc = demo_vpc.vpc,
        #     tags = {
        #         "Name": "demo_pvt_rtb"
        #     }
        # )

        # demo_pub_rtb = RoutetableConstruct(
        #     self,
        #     "demo_pub_rtb",
        #     vpc = demo_vpc.vpc,
        #     tags = {
        #         "Name": "demo_pub_rtb"
        #     }
        # )

        # demo_pvt_rtb_snt_asociation_1a = Routetable_Snt_Association_Construct(
        #     self,
        #     "demo_pvt_rtb_snt_asociation_1a",
        #     subnet = demo_pvt_snt_1a.subnet,
        #     route_table= demo_pvt_rtb.route_table
        # )

        # demo_pvt_rtb_snt_asociation_1b = Routetable_Snt_Association_Construct(
        #     self,
        #     "demo_pvt_rtb_snt_asociation_1b",
        #     subnet = demo_pvt_snt_1b.subnet,
        #     route_table= demo_pvt_rtb.route_table
        # )

        # demo_pub_rtb_snt_asociation_1a = Routetable_Snt_Association_Construct(
        #     self,
        #     "demo_pub_rtb_snt_asociation_1a",
        #     subnet = demo_pub_snt_1a.subnet,
        #     route_table= demo_pub_rtb.route_table
        # )

        # demo_pub_rtb_snt_asociation_1b = Routetable_Snt_Association_Construct(
        #     self,
        #     "demo_pub_rtb_snt_asociation_1b",
        #     subnet = demo_pub_snt_1b.subnet,
        #     route_table= demo_pub_rtb.route_table
        # )

        # demo_igw = InternetGatewayConstruct(
        #     self,
        #     "demo_igw",
        #     vpc=demo_vpc.vpc,
        #     tags = {
        #         "Name": "demo_igw"
        #     }
        # )

        # demo_natgateway_1a = NatGatewayConstruct(
        #     self,
        #     "demo_natgateway_1a",
        #     public_subnet= demo_pvt_snt_1a.subnet,
        #     EIP_tags = {
        #         "Name": "demo_natgateway_1a_eip"
        #     },
        #     Natgateway_tags = {
        #         "Name": "demo_natgateway_1a"
        #     }
        # )

        # demo_natgateway_1b = NatGatewayConstruct(
        #     self,
        #     "demo_natgateway_1b",
        #     public_subnet= demo_pvt_snt_1b.subnet,
        #     EIP_tags = {
        #         "Name": "demo_natgateway_1b_eip"
        #     },
        #     Natgateway_tags = {
        #         "Name": "demo_natgateway_1b"
        #     }
        # )

        # demo_tgw = TransitGatewayConstruct(
        #     self,
        #     "demo_tgw",
        #     tags = {
        #         "Name": "demo_tgw"
        #     }
        # )

        # demo_tgw_share = TransitGatewayShareConstruct(
        #     self,
        #     "demo_tgw_share",
        #     transit_gateway_arn= demo_tgw.transit_gateway.attr_transit_gateway_arn,
        #     target_account_id= "032401369172", 
        #     share_name= "tgw-to-agentic-share", 
        #     allow_external_principals = True
        # )

        # demo_tgw_rtb = TgwRouteTableConstrcut(
        #     self,
        #     "demo_tgw_rtb",
        #     transit_gateway_id = demo_tgw.transit_gateway.ref,
        #     tags = {
        #         "Name": "demo_tgw_rtb"
        #     }
        # )

        # demo_alert_log_grp = CloudWatchLogGroup(
        #     self,
        #     "demo_alert_log_grp",
        #     log_group_name = "demo_alert_log_grp",
        #     retention= 30
        # )

        # demo_flow_log_grp = CloudWatchLogGroup(
        #     self,
        #     "demo_flow_log_grp",
        #     log_group_name = "demo_flow_log_grp",
        #     retention= 30
        # )

        # demo_firewall_policy = FirewallPolicyConstruct(
        #     self,
        #     "demo_firewall_policy",
        #     firewall_policy_name = "demo-firewall-policy"
        # )

        # demo_firewall = NetworkFirewallConstruct(
        #     self,
        #     "demo_firewall",
        #     firewall_name = "demo-firewall",
        #     firewall_policy_arn = demo_firewall_policy.policy.attr_firewall_policy_arn,
        #     firewall_subnet_ids = [
        #         demo_pvt_snt_1a.subnet.ref,
        #         demo_pvt_snt_1b.subnet.ref
        #     ],
        #     alert_log_group_name = "demo_alert_log_grp",
        #     flow_log_group_name = "demo_flow_log_grp",
        #     vpc_id = demo_vpc.vpc.ref
        # )





        

        
















