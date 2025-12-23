from constructs import Construct
from aws_cdk import (
    aws_ec2 as ec2,
    Stack,
)

class NetworkStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, app_prefix: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        # Create VPC
        self.vpc = ec2.Vpc(
            self,
            "VPC",
            vpc_name=f"{app_prefix}-vpc",
            ip_addresses=ec2.IpAddresses.cidr("10.10.0.0/16"),
            enable_dns_hostnames=True,
            enable_dns_support=True,
            # Create VPC without subnets
            subnet_configuration=[]
        )
        
        # Get availability zones (first 2)
        azs = self.availability_zones[:2]
        
        # Create Internet Gateway
        self.igw = ec2.CfnInternetGateway(
            self,
            "InternetGateway",
            tags=[{"key": "Name", "value": f"{app_prefix}-igw"}]
        )
        
        # Attach Internet Gateway to VPC
        ec2.CfnVPCGatewayAttachment(
            self,
            "IGWAttachment",
            vpc_id=self.vpc.vpc_id,
            internet_gateway_id=self.igw.ref  # Fixed: Use .ref instead of .attr_internet_gateway_id
        )
        
        # Create Public Subnets
        self.public_subnets = []
        for i, az in enumerate(azs):
            subnet = ec2.CfnSubnet(
                self,
                f"PublicSubnet{i+1}",
                availability_zone=az,
                cidr_block=f"10.10.{i}.0/24",
                vpc_id=self.vpc.vpc_id,
                map_public_ip_on_launch=True,
                tags=[{"key": "Name", "value": f"{app_prefix}-public-subnet-{i+1}"}]
            )
            self.public_subnets.append(subnet)
        
        # Create Private Subnets
        self.private_subnets = []
        for i, az in enumerate(azs):
            subnet = ec2.CfnSubnet(
                self,
                f"PrivateSubnet{i+1}",
                availability_zone=az,
                cidr_block=f"10.10.{i+10}.0/24",  # 10.10.10.0/24, 10.10.11.0/24
                vpc_id=self.vpc.vpc_id,
                map_public_ip_on_launch=False,
                tags=[{"key": "Name", "value": f"{app_prefix}-private-subnet-{i+1}"}]
            )
            self.private_subnets.append(subnet)
        
        # Create EIP for NAT Gateway first
        self.nat_eip = ec2.CfnEIP(
            self,
            "NATGatewayEIP",
            domain="vpc",
            tags=[{"key": "Name", "value": f"{app_prefix}-nat-eip"}]
        )
        
        # Create NAT Gateway (in first public subnet)
        self.nat_gateway = ec2.CfnNatGateway(
            self,
            "NATGateway",
            subnet_id=self.public_subnets[0].ref,  # Fixed: Use .ref instead of .attr_subnet_id
            allocation_id=self.nat_eip.attr_allocation_id,
            tags=[{"key": "Name", "value": f"{app_prefix}-nat-gateway"}]
        )
        
        # Create Route Tables
        # Public Route Table
        self.public_route_table = ec2.CfnRouteTable(
            self,
            "PublicRouteTable",
            vpc_id=self.vpc.vpc_id,
            tags=[{"key": "Name", "value": f"{app_prefix}-public-rt"}]
        )
        
        # Add route to Internet Gateway
        ec2.CfnRoute(
            self,
            "PublicRoute",
            route_table_id=self.public_route_table.ref,  # Fixed: Use .ref instead of .attr_route_table_id
            destination_cidr_block="0.0.0.0/0",
            gateway_id=self.igw.ref  # Fixed: Use .ref instead of .attr_internet_gateway_id
        )
        
        # Associate public subnets with public route table
        for i, subnet in enumerate(self.public_subnets):
            ec2.CfnSubnetRouteTableAssociation(
                self,
                f"PublicSubnetRTAssoc{i+1}",
                subnet_id=subnet.ref,  # Fixed: Use .ref instead of .attr_subnet_id
                route_table_id=self.public_route_table.ref  # Fixed: Use .ref instead of .attr_route_table_id
            )
        
        # Private Route Table
        self.private_route_table = ec2.CfnRouteTable(
            self,
            "PrivateRouteTable",
            vpc_id=self.vpc.vpc_id,
            tags=[{"key": "Name", "value": f"{app_prefix}-private-rt"}]
        )
        
        # Add route to NAT Gateway
        ec2.CfnRoute(
            self,
            "PrivateRoute",
            route_table_id=self.private_route_table.ref,  # Fixed: Use .ref instead of .attr_route_table_id
            destination_cidr_block="0.0.0.0/0",
            nat_gateway_id=self.nat_gateway.ref  # Fixed: Use .ref instead of .attr_nat_gateway_id
        )
        
        # Associate private subnets with private route table
        for i, subnet in enumerate(self.private_subnets):
            ec2.CfnSubnetRouteTableAssociation(
                self,
                f"PrivateSubnetRTAssoc{i+1}",
                subnet_id=subnet.ref,  # Fixed: Use .ref instead of .attr_subnet_id
                route_table_id=self.private_route_table.ref  # Fixed: Use .ref instead of .attr_route_table_id
            )
        
        # Create NACL for Public Subnets using CFN construct for consistency
        self.public_nacl = ec2.CfnNetworkAcl(
            self,
            "PublicNACL",
            vpc_id=self.vpc.vpc_id,
            tags=[{"key": "Name", "value": f"{app_prefix}-public-nacl"}]
        )
        
        # Public NACL Rules - Inbound Rules
        ec2.CfnNetworkAclEntry(
            self,
            "PublicNACLInboundHTTP",
            network_acl_id=self.public_nacl.ref,
            rule_number=100,
            protocol=6,  # TCP
            rule_action="allow",
            cidr_block="0.0.0.0/0",
            port_range=ec2.CfnNetworkAclEntry.PortRangeProperty(from_=80, to=80)
        )
        
        ec2.CfnNetworkAclEntry(
            self,
            "PublicNACLInboundHTTPS",
            network_acl_id=self.public_nacl.ref,
            rule_number=110,
            protocol=6,  # TCP
            rule_action="allow",
            cidr_block="0.0.0.0/0",
            port_range=ec2.CfnNetworkAclEntry.PortRangeProperty(from_=443, to=443)
        )
        
        ec2.CfnNetworkAclEntry(
            self,
            "PublicNACLInboundSSH",
            network_acl_id=self.public_nacl.ref,
            rule_number=120,
            protocol=6,  # TCP
            rule_action="allow",
            cidr_block="0.0.0.0/0",
            port_range=ec2.CfnNetworkAclEntry.PortRangeProperty(from_=22, to=22)
        )
        
        # Allow ephemeral ports for return traffic
        ec2.CfnNetworkAclEntry(
            self,
            "PublicNACLInboundEphemeral",
            network_acl_id=self.public_nacl.ref,
            rule_number=130,
            protocol=6,  # TCP
            rule_action="allow",
            cidr_block="0.0.0.0/0",
            port_range=ec2.CfnNetworkAclEntry.PortRangeProperty(from_=1024, to=65535)
        )

        ec2.CfnNetworkAclEntry(
            self,
            "PublicNACLOutboundICMP",
            network_acl_id=self.public_nacl.ref,
            rule_number=140,
            protocol=1,  # ICMP
            rule_action="allow",
            cidr_block="0.0.0.0/0",
            icmp=ec2.CfnNetworkAclEntry.IcmpProperty(
                type=8,  # Echo Request
                code=-1  # All codes
            )
        )

        # Allow ICMP Echo Reply back IN
        ec2.CfnNetworkAclEntry(
            self,
            "PublicNACLInboundICMPReply",
            network_acl_id=self.public_nacl.ref,
            rule_number=150,
            protocol=1,  # ICMP
            rule_action="allow",
            cidr_block="0.0.0.0/0",
            icmp=ec2.CfnNetworkAclEntry.IcmpProperty(
                type=0,  # Echo Reply
                code=-1  # All codes
            )
        )
        
        # Outbound Rules - Allow all outbound traffic
        ec2.CfnNetworkAclEntry(
            self,
            "PublicNACLOutboundAll",
            network_acl_id=self.public_nacl.ref,
            rule_number=140,
            protocol=-1,  # All protocols
            rule_action="allow",
            cidr_block="0.0.0.0/0",
            egress=True,
        )
        
        # Create NACL for Private Subnets
        self.private_nacl = ec2.CfnNetworkAcl(
            self,
            "PrivateNACL",
            vpc_id=self.vpc.vpc_id,
            tags=[{"key": "Name", "value": f"{app_prefix}-private-nacl"}]
        )
        
        # Private NACL Rules - Allow inbound from VPC CIDR
        ec2.CfnNetworkAclEntry(
            self,
            "PrivateNACLInboundFromVPC",
            network_acl_id=self.private_nacl.ref,
            rule_number=100,
            protocol=-1,  # All protocols
            rule_action="allow",
            cidr_block="10.10.0.0/16"
        )
        
        # Allow ephemeral ports for return traffic from internet
        ec2.CfnNetworkAclEntry(
            self,
            "PrivateNACLInboundEphemeral",
            network_acl_id=self.private_nacl.ref,
            rule_number=110,
            protocol=6,  # TCP
            rule_action="allow",
            cidr_block="0.0.0.0/0",
            port_range=ec2.CfnNetworkAclEntry.PortRangeProperty(from_=1024, to=65535)
        )
        
        # Private NACL Outbound Rules
        ec2.CfnNetworkAclEntry(
            self,
            "PrivateNACLOutboundToVPC",
            network_acl_id=self.private_nacl.ref,
            rule_number=120,
            protocol=-1,  # All protocols
            rule_action="allow",
            cidr_block="10.10.0.0/16",
            egress=True,
        )

        # Allow outbound HTTP/HTTPS for updates and downloads
        ec2.CfnNetworkAclEntry(
            self,
            "PrivateNACLOutboundHTTP",
            network_acl_id=self.private_nacl.ref,
            rule_number=130,
            protocol=6,  # TCP
            rule_action="allow",
            cidr_block="0.0.0.0/0",
            egress=True,
            port_range=ec2.CfnNetworkAclEntry.PortRangeProperty(from_=80, to=80)
        )
        
        ec2.CfnNetworkAclEntry(
            self,
            "PrivateNACLOutboundHTTPS",
            network_acl_id=self.private_nacl.ref,
            rule_number=140,
            protocol=6,  # TCP
            rule_action="allow",
            cidr_block="0.0.0.0/0",
            egress=True,
            port_range=ec2.CfnNetworkAclEntry.PortRangeProperty(from_=443, to=443)
        )
        
        # Allow outbound DNS
        ec2.CfnNetworkAclEntry(
            self,
            "PrivateNACLOutboundDNS",
            network_acl_id=self.private_nacl.ref,
            rule_number=150,
            protocol=17,  # UDP
            rule_action="allow",
            cidr_block="0.0.0.0/0",
            egress=True,
            port_range=ec2.CfnNetworkAclEntry.PortRangeProperty(from_=53, to=53)
        )
        
        # Associate NACLs with subnets using CFN constructs
        for i, subnet in enumerate(self.public_subnets):
            ec2.CfnSubnetNetworkAclAssociation(
                self,
                f"PublicSubnetNACLAssoc{i+1}",
                subnet_id=subnet.ref,  # Fixed: Use .ref instead of .attr_subnet_id
                network_acl_id=self.public_nacl.ref  # Fixed: Use CFN construct and .ref
            )
            
        for i, subnet in enumerate(self.private_subnets):
            ec2.CfnSubnetNetworkAclAssociation(
                self,
                f"PrivateSubnetNACLAssoc{i+1}",
                subnet_id=subnet.ref,  # Fixed: Use .ref instead of .attr_subnet_id
                network_acl_id=self.private_nacl.ref  # Fixed: Use CFN construct and .ref
            )
        
        # Export important values for other stacks
        self.vpc_id = self.vpc.vpc_id
        self.public_subnet_ids = [subnet.ref for subnet in self.public_subnets]  # Fixed: Use .ref
        self.private_subnet_ids = [subnet.ref for subnet in self.private_subnets]  # Fixed: Use .ref