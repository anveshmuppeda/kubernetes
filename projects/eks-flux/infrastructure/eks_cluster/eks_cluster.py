from aws_cdk.lambda_layer_kubectl_v30 import KubectlV30Layer
from aws_cdk import (
    Stack,
    aws_eks as eks,
    aws_ec2 as ec2,
    aws_iam as iam,
)
from constructs import Construct


class KubernetesStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, network_stack, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.network_stack = network_stack

        masters_role = iam.Role(
            self,
            "eks-admin",
            role_name="aws-eks-admin",
            assumed_by=iam.CompositePrincipal(
                iam.ServicePrincipal(service="eks.amazonaws.com"),
                iam.AnyPrincipal(),  # importent, else a SSO user can't assume
            ),
        )
        masters_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("AdministratorAccess")
        )
        readonly_role = iam.Role(
            self,
            "eks-readonly",
            role_name="aws-eks-readonly",
            assumed_by=iam.CompositePrincipal(
                iam.ServicePrincipal(service="eks.amazonaws.com"),
                iam.AnyPrincipal(),  # importent, else a SSO user can't assume
            ),
        )
        readonly_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("AdministratorAccess")
        )

        # Convert CFN subnets to ISubnet objects that EKS can use
        private_subnets = []
        for i, cfn_subnet in enumerate(network_stack.private_subnets):
            subnet = ec2.Subnet.from_subnet_attributes(
                self,
                f"PrivateSubnet{i+1}Import",
                subnet_id=cfn_subnet.ref,
                availability_zone=cfn_subnet.availability_zone,
                route_table_id=network_stack.private_route_table.ref
            )
            private_subnets.append(subnet)

        public_subnets = []
        for i, cfn_subnet in enumerate(network_stack.public_subnets):
            subnet = ec2.Subnet.from_subnet_attributes(
                self,
                f"PublicSubnet{i+1}Import",
                subnet_id=cfn_subnet.ref,
                availability_zone=cfn_subnet.availability_zone,
                route_table_id=network_stack.public_route_table.ref
            )
            public_subnets.append(subnet)

        # Create VPC selection for EKS
        vpc_subnets = [
            ec2.SubnetSelection(subnets=private_subnets),
            ec2.SubnetSelection(subnets=public_subnets)
        ]

        cluster = eks.Cluster(
            self,
            "aws-eks",
            version=eks.KubernetesVersion.V1_30,
            masters_role=masters_role,
            cluster_name="aws-eks-cluster",
            kubectl_layer=KubectlV30Layer(self, "kubectl"),
            default_capacity=0,
            cluster_logging=[
                eks.ClusterLoggingTypes.API,
                eks.ClusterLoggingTypes.AUTHENTICATOR,
                eks.ClusterLoggingTypes.SCHEDULER,
                eks.ClusterLoggingTypes.AUDIT,
                eks.ClusterLoggingTypes.CONTROLLER_MANAGER,
            ],
            vpc=network_stack.vpc,
            vpc_subnets=vpc_subnets,
        )

        masters_role.grant_assume_role(cluster.admin_role)

        cluster.aws_auth.add_role_mapping(
            readonly_role, groups=["system:authenticated"]
        )

        self.__add_nodegroup(cluster=cluster)
        self.__add_addon(cluster=cluster)
        self.__add_readonly_member(
            cluster=cluster, readonly_role_arn=readonly_role.role_arn
        )

    def __add_nodegroup(self, cluster: eks.Cluster):
        instance_type_name = "t3.medium"

        subnet_selection = ec2.SubnetSelection(subnets=[
            subnet for subnet in cluster.vpc.private_subnets
        ])

        self.nodegroup = eks.Nodegroup(
            self,
            "all-ng",
            cluster=cluster,
            nodegroup_name="primary-node-group",
            instance_types=[ec2.InstanceType(instance_type_name)],
            min_size=1,
            max_size=3,
            disk_size=100,
            subnets=subnet_selection,
            labels={
                "instance-type": instance_type_name,
            },
        )

    def __add_addon(self, cluster: eks.Cluster):
        eks.CfnAddon(
            self,
            "vpc-cni-addon",
            addon_name="vpc-cni",
            cluster_name=cluster.cluster_name,
        )
        eks.CfnAddon(
            self,
            "coredns-addon",
            addon_name="coredns",
            cluster_name=cluster.cluster_name,
        )
        eks.CfnAddon(
            self,
            "kube-proxy-addon",
            addon_name="kube-proxy",
            cluster_name=cluster.cluster_name,
        )
        eks.CfnAddon(
            self,
            "aws-ebs-csi-driver-addon",
            addon_name="aws-ebs-csi-driver",
            cluster_name=cluster.cluster_name,
        )

    def __add_readonly_member(self, cluster: eks.Cluster, readonly_role_arn: str):
        cluster.add_manifest(
            "cluster-role",
            {
                "apiVersion": "rbac.authorization.k8s.io/v1",
                "kind": "ClusterRole",
                "metadata": {
                    "name": "eks-access-cluster-role",
                    "namespace": "kube-system",
                },
                "rules": [
                    {
                        "apiGroups": [""],
                        "resources": [
                            "configmaps",
                            "services",
                            "pods",
                            "persistentvolumes",
                            "namespaces",
                        ],
                        "verbs": ["get", "list", "watch"],
                    },
                    {
                        "apiGroups": [""],
                        "resources": ["pods/log"],
                        "verbs": ["get", "list"],
                    },
                    {
                        "apiGroups": [""],
                        "resources": ["pods/portforward", "services/portforward"],
                        "verbs": ["create"],
                    },
                ],
            },
        )

        cluster.add_manifest(
            "cluster-role-binding",
            {
                "apiVersion": "rbac.authorization.k8s.io/v1",
                "kind": "ClusterRoleBinding",
                "metadata": {
                    "name": "iam-cluster-role-binding",
                    "namespace": "kube-system",
                },
                "roleRef": {
                    "apiGroup": "rbac.authorization.k8s.io",
                    "kind": "ClusterRole",
                    "name": "eks-access-cluster-role",
                },
                "subjects": [
                    {
                        "kind": "User",
                        "name": readonly_role_arn,
                        "apiGroup": "rbac.authorization.k8s.io",
                    }
                ],
            },
        )