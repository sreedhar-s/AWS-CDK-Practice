#!/usr/bin/env python3
import aws_cdk as cdk
from stacks.network_vpc_stack import NetworkStack
from stacks.workload_vpc_stack import WorkloadNetworkStack
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

app.synth()

