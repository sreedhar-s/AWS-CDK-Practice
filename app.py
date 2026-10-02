#!/usr/bin/env python3
import aws_cdk as cdk
from stacks.network_vpc_stack import NetworkStack
from stacks.workload_vpc_stack import WorkloadNetworkStack
from stacks.management_stack import ManagementStack
from constructs import Construct

app = cdk.App()
NetworkStack(
    app, 
    "NetworkStack",
    env=cdk.Environment( 
        account="791614298327", 
        region="ap-southeast-1"
    )
)

WorkloadNetworkStack(
    app,
    "WorkloadNetworkStack",
    env=cdk.Environment( 
        account="032401369172", 
        region="ap-southeast-1"
    )
)

ManagementStack(
    app,
    "ManagementStack"
    env=cdk.Environment( 
        account="641833687551",
    )
)

app.synth()

