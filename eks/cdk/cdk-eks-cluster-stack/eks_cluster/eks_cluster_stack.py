from constructs import Construct
from aws_cdk.lambda_layer_kubectl_v33 import KubectlV33Layer
from aws_cdk import (
    Duration,
    Stack,
    aws_iam as iam,
    aws_ec2 as ec2,
    aws_eks as eks,
    aws_s3 as s3,
    RemovalPolicy,
)

class EksClusterStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, app_prefix: str, network_stack, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        # Store network stack reference
        self.network_stack = network_stack

        # Create IAM roles for EKS cluster
        self.__create_iam_roles(app_prefix=app_prefix)

        # Create EKS cluster with specified configurations
        self.__create_eks_cluster(app_prefix=app_prefix)

        # Add node groups and addons
        self.__add_nodegroup(cluster=self.cluster, app_prefix=app_prefix)
        self.__add_addon(cluster=self.cluster)

        # Create demo Pod Identity Association
        self.__create_pod_identity_association(app_prefix=app_prefix)
    
    def __create_iam_roles(self, app_prefix: str) -> None:
        """
        Create IAM roles for EKS cluster operations.
        :param app_prefix: Prefix for naming resources.
        """

        # Create EKS Service Role
        self.eks_service_role = iam.Role(
            self,
            "EKSServiceRole",
            role_name=f"{app_prefix}-eks-service-role",
            assumed_by=iam.ServicePrincipal("eks.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonEKSClusterPolicy")
            ]
        )

        # Create Node Group Role
        self.nodegroup_role = iam.Role(
            self,
            "NodeGroupRole",
            role_name=f"{app_prefix}-eks-nodegroup-role",
            assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonEKSWorkerNodePolicy"),
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonEKS_CNI_Policy"),
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonEC2ContainerRegistryReadOnly"),
                iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AmazonEBSCSIDriverPolicy")
            ]
        )

        # Create demo role for Pod Identity Association
        self.demo_pod_role = iam.Role(
            self,
            "DemoPodRole",
            role_name=f"{app_prefix}-demo-pod-role",
            assumed_by=iam.ServicePrincipal("pods.eks.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3ReadOnlyAccess")
            ]
        )

        # Add custom policy for demo purposes
        self.demo_pod_role.add_to_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                actions=[
                    "s3:ListBucket",
                    "s3:GetObject",
                    "secretsmanager:GetSecretValue",
                    "ssm:GetParameter"
                ],
                resources=["*"]
            )
        )

        # Create masters role for demo cluster access
        self.masters_role = iam.Role(
            self,
            "EKSMastersRole",
            role_name=f"{app_prefix}-eks-masters-role",
            assumed_by=iam.CompositePrincipal(
                iam.AccountRootPrincipal(),
                iam.AnyPrincipal(),  # WARNING: This allows ANYONE to assume this role
            ),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonEKSClusterPolicy")
            ]
        )
  
    def __create_eks_cluster(self, app_prefix: str) -> None:
        """
        Create EKS cluster with specified configurations.
        :param app_prefix: Prefix for naming resources.
        """

        # Use public subnets for cluster endpoint
        public_subnets = []
        for i, cfn_subnet in enumerate(self.network_stack.public_subnets):
            subnet = ec2.Subnet.from_subnet_attributes(
                self,
                f"PublicSubnet{i+1}Import",
                subnet_id=cfn_subnet.ref,
                availability_zone=cfn_subnet.availability_zone,
                route_table_id=self.network_stack.public_route_table.ref
            )
            public_subnets.append(subnet)

        # Create EKS Cluster
        self.cluster = eks.Cluster(
            self,
            "EKSCluster",
            cluster_name=f"{app_prefix}-eks-cluster",
            version=eks.KubernetesVersion.V1_32,
            vpc=self.network_stack.vpc,
            vpc_subnets=[ec2.SubnetSelection(subnets=public_subnets)],
            role=self.eks_service_role,
            masters_role=self.masters_role,
            kubectl_layer=KubectlV33Layer(self, "kubectl"),
            default_capacity=0,
            endpoint_access=eks.EndpointAccess.PUBLIC_AND_PRIVATE,
            cluster_logging=[
                eks.ClusterLoggingTypes.API,
                eks.ClusterLoggingTypes.AUTHENTICATOR,
                eks.ClusterLoggingTypes.SCHEDULER,
                eks.ClusterLoggingTypes.AUDIT,
                eks.ClusterLoggingTypes.CONTROLLER_MANAGER,
            ],
        )

        # Add demo GitHub IAM Role to the cluster access
        self.cluster.aws_auth.add_role_mapping(
            role=iam.Role.from_role_arn(
                self,
                "DemoGitHubRole",
                role_arn=f"arn:aws:iam::{self.account}:role/demo-github-role"
            ),
            groups=["system:masters"],
            username="DemoGitHubUser"
        )

        # Add demo IAM User to the cluster access
        self.cluster.aws_auth.add_user_mapping(
            user=iam.User.from_user_arn(
                self,
                "DemoEKSUser",
                user_arn=f"arn:aws:iam::{self.account}:user/demo-eks-user"
            ),
            groups=["system:masters"],
            username="DemoEKSAdminUser"
        )

    def __add_nodegroup(self, cluster: eks.Cluster, app_prefix: str):
        instance_type_name = "t3.medium"

        # Get public subnets for node group
        public_subnets = []
        for i, cfn_subnet in enumerate(self.network_stack.public_subnets):
            subnet = ec2.Subnet.from_subnet_attributes(
                self,
                f"NodeGroupPublicSubnet{i+1}",
                subnet_id=cfn_subnet.ref,
                availability_zone=cfn_subnet.availability_zone
            )
            public_subnets.append(subnet)

        # Create managed node group
        self.nodegroup = eks.Nodegroup(
            self,
            "PrimaryNodeGroup",
            cluster=cluster,
            nodegroup_name=f"{app_prefix}-primary-nodegroup",
            node_role=self.nodegroup_role,
            instance_types=[ec2.InstanceType(instance_type_name)],
            subnets=ec2.SubnetSelection(subnets=public_subnets),
            min_size=1,
            max_size=5,
            desired_size=2,
            disk_size=100,
            ami_type=eks.NodegroupAmiType.AL2_X86_64,
            capacity_type=eks.CapacityType.ON_DEMAND,
            labels={
                "instance-type": instance_type_name,
                "nodegroup-type": "primary"
            },
            tags={
                "Name": f"{app_prefix}-primary-nodegroup",
                "Environment": "demo"
            }
        )

    def __add_addon(self, cluster: eks.Cluster):
        # VPC CNI Addon
        eks.CfnAddon(
            self,
            "VPCCNIAddon",
            addon_name="vpc-cni",
            cluster_name=cluster.cluster_name,
            resolve_conflicts="OVERWRITE"
        )
        
        # CoreDNS Addon
        eks.CfnAddon(
            self,
            "CoreDNSAddon",
            addon_name="coredns",
            cluster_name=cluster.cluster_name,
            resolve_conflicts="OVERWRITE"
        )
        
        # Kube Proxy Addon
        eks.CfnAddon(
            self,
            "KubeProxyAddon",
            addon_name="kube-proxy",
            cluster_name=cluster.cluster_name,
            resolve_conflicts="OVERWRITE"
        )
        
        # EBS CSI Driver Addon
        eks.CfnAddon(
            self,
            "EBSCSIDriverAddon",
            addon_name="aws-ebs-csi-driver",
            cluster_name=cluster.cluster_name,
            resolve_conflicts="OVERWRITE"
        )

        # Pod Identity Association Addon
        eks.CfnAddon(
            self,
            "PodIdentityAssociationAddon",
            addon_name="eks-pod-identity-agent",
            cluster_name=cluster.cluster_name,
            resolve_conflicts="OVERWRITE"
        )
    
  
    def __create_pod_identity_association(self, app_prefix: str) -> None:
        """
        Create Pod Identity Association for demo purposes.
        :param app_prefix: Prefix for naming resources.
        """

        # Create Pod Identity Association for demo
        self.pod_identity_association = eks.CfnPodIdentityAssociation(
            self,
            "DemoPodIdentityAssociation",
            cluster_name=self.cluster.cluster_name,
            namespace="default",
            service_account="demo-service-account",
            role_arn=self.demo_pod_role.role_arn,
            tags=[
                {
                    "key": "Name",
                    "value": f"{app_prefix}-demo-pod-identity"
                },
                {
                    "key": "Environment",
                    "value": "demo"
                }
            ]
        )