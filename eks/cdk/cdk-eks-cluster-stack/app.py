#!/usr/bin/env python3

import aws_cdk as cdk
from aws_cdk import Tags

from eks_cluster.eks_cluster_stack import EksClusterStack
from eks_cluster.network_stack import NetworkStack

app = cdk.App()

APP_PREFIX = "eks-demo"

network_stack = NetworkStack(
    app, 
    "NetworkStack", 
    app_prefix=APP_PREFIX
)

eks_stack = EksClusterStack(
    app, 
    "EksClusterStack",
    app_prefix=APP_PREFIX,
    network_stack=network_stack
)

Tags.of(app).add("Application", APP_PREFIX)
Tags.of(app).add("Owner", "Anvesh Muppeda")
Tags.of(app).add("Environment", "Sandbox")
Tags.of(app).add("Project", "AWSInfra")
Tags.of(app).add("ManagedBy", "CDK")

eks_stack.add_dependency(network_stack)

app.synth()