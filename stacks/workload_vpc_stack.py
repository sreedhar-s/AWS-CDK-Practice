from aws_cdk import Stack 
from constructs import Construct

from aws_constructs.vpc import VpcConstruct
from aws_constructs.subnet import SubnetConstruct
from aws_constructs.tgw_attachment import TransitGatewayAttachmentConstruct

class WorkloadNetworkStack(Stack):
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

        # demo_tgw_att = TransitGatewayAttachmentConstruct(
        #     self,
        #     "demo_tgw_att",
        #     transit_gateway_id= "tgw-0171b3ba72a3c02db",
        #     vpc_id = demo_vpc.vpc.ref, 
        #     subnet_ids= [
        #         demo_pvt_snt_1a.subnet.ref,
        #         demo_pvt_snt_1b.subnet.ref
        #     ],
        #     tags = {
        #         "Name": "demo_tgw_att"
        #     } 
        # )









        

        
















