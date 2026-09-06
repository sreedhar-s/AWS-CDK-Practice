from typing import Dict, Optional
from aws_cdk import ( aws_ec2 as ec2 )
from constructs import Construct

class Routetable_Snt_Association_Construct(Construct):
    def __init__( 
            self, 
            scope: Construct, 
            construct_id: str, *, 
            subnet: ec2.CfnSubnet,
            route_table: ec2.CfnRouteTable
        ) -> None:

        super().__init__(scope, construct_id)

        self.route_table_snt_association = ec2.CfnSubnetRouteTableAssociation( 
            self, 
            "route_table_snt_association",
            subnet_id = subnet.ref,
            route_table_id = route_table.ref
        )

