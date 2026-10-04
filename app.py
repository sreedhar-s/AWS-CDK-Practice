#!/usr/bin/env python3
import aws_cdk as cdk
from constructs import Construct
from stacks.network_vpc_stack import NetworkStack
from stacks.workload_stack import WorkloadStack
from stacks.management_stack import ManagementStack

app = cdk.App()
NetworkStack(
    app, 
    "NetworkStack",
    env=cdk.Environment( 
        account="791614298327", 
        region="ap-southeast-1"
    )
)

WorkloadStack(
    app,
    "WorkloadStack",
    env=cdk.Environment( 
        account="032401369172", 
        region="ap-southeast-1"
    )
)

# ManagementStack(
#     app,
#     "ManagementStack",
#     env=cdk.Environment( 
#         account="641833687551"
#     )
# )

app.synth()

