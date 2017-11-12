class VpcResource:
    """Class object to store VPC resources based on VPC ID
    
    This class will store VPC information along with all the subnet
    information attached to the VPC, all the route tables, 
    and the internet gateway. It only stores information that is
    needed by the terraform module.
    """
    
    def __init__(self, vpcid):
        
        # VPC ID of this object
        self.vpcid = vpcid
        
        # VPC Name (if any)
        self.name = ''
        
        # VPC CIDR Range
        self.cidr = ''
        
        # List of AZs
        self.azs = []
        
        # List of private subnets CIDR range
        self.private_subnets = []
        
        # List of public subnets CIDR Range
        self.public_subnets = []
        
        self.enable_nat_gateway = False
        self.enable_vpn_gateway = False
        
        # List of tags for the VPC
        self.vpc_tags = {}
        
        # List of tags for private subnets
        self.private_subnet_tags = []
        
        # List of tags for public subnets
        self.public_subnet_tags = []
        
        # List of tags for the private route tables
        self.private_route_tags = []
        
        # List of tags for the public route tables
        self.public_route_tags = []
        
        # List of subnet IDs attached to this VPC
        self.subnet_ids = []
        
        # List of route table IDs attached to this VPC
        self.route_table_ids = []
        
        # List of internet gateways attached to this VPC
        self.internet_gateway_id = ''
        

class GetResources:
    """Gather all VPC resources in a VpcResource object"""
    
    def __init__(self, session):
        
        self.session = session
        self.client = self.session.client('ec2')
        
        # Declare the VPC object
        self.vpc_obj = None
        
    def get_vpcs(self):
        """Gather all VPC information and return it"""
        
        # Get all the VPCs
        resources = self.client.describe_vpcs()['Vpcs']
        
        # Store the VpcResource objects in a list
        vpcs = []
        
        # Loop the VPC resources and gather all other resources
        for vpc in resources:
        
            # Instantiate the VpcResource using the VPC ID and
            # store the VPC Object for use by other methods
            self.vpc_obj = VpcResource(vpc['VpcId'])
            
            # Get VPC CIDR Range
            self.vpc_obj.cidr = vpc['CidrBlock']
            
            # Get the tag key 'Name'
            for tag in vpc['Tags']:
                
                # If the tag key is 'Name', store the value
                # in the VpcResource object
                if tag['Key'] == 'Name':
                    self.vpc_obj.name = tag['Value']
            
            # Get all the subnet resource information and store it
            # in the VpcResource object
            self.get_subnets()
            
            # Get all route tables associated to this VPC
            self.get_route_tables()
            
            # Get all internet gateways associated with this VPC
            self.get_internet_gateways()
            
            # Append the VpcResource object to the vpcs list
            vpcs.append(self.vpc_obj)
        
        # Return list of VpcResource objects
        return vpcs
        
    def get_subnets(self):
        """Gather all subnet resources belonging to a specfic VPC ID"""
        
        # Get all subnets beloging to this VPC
        subnets = self.client.describe_subnets(
                Filters = [
                        {
                            'Name': 'vpc-id',
                            'Values': [
                                    self.vpc_obj.vpcid
                                ]
                        }
                    ]
            )['Subnets']
            
        # Loop through all the subnets
        for subnet in subnets:
            
            # Get the subnet ID
            sub_id = subnet['SubnetId']
            
            # Get the boto3 subnet resource
            ec2 = self.session.resource('ec2')
            sub = ec2.Subnet(sub_id)
            
            # Gather all the subnet details
            self.vpc_obj.azs.append(sub.availability_zone)
            self.vpc_obj.public_subnets.append(sub.cidr_block)
            self.vpc_obj.public_subnet_tags.append(sub.tags)
            
    def get_route_tables(self):
        """Gather all route table resources belonging to a specific VPC ID"""
        
        # Get route tables for this VPC
        route_tables = self.client.describe_route_tables(
                Filters = [
                        {
                            'Name': 'vpc-id',
                            'Values': [
                                    self.vpc_obj.vpcid
                                ]
                        }
                    ]
            )['RouteTables']
            
        # Loop through all the route tables
        for route in route_tables:
            
            # Get the route table ID
            route_id = route['RouteTableId']
            
            # If there are no subnet associations, skip this route table
            if 'SubnetId' not in route['Associations'][0]:
                continue
            
            # Store the route table IDs in a list in the VpcResource object
            self.vpc_obj.route_table_ids.append(route_id)
            
            # Storage tag information
            self.vpc_obj.public_route_tags = route['Tags']
            
    def get_internet_gateways(self):
        """Gather all internet gateways belonging to this specific VPC ID"""
        
        # Get internet gateways for this VPC
        igws = self.client.describe_internet_gateways(
            Filters = [
                        {
                            'Name': 'attachment.vpc-id',
                            'Values': [
                                    self.vpc_obj.vpcid
                                ]
                        }
                    ]
            )['InternetGateways']
            
            
        # Check if there's an internet gateway
        if igws:
            # Store the internet gateway ID in the Vpc Resource Object
            self.vpc_obj.internet_gateway_id = igws[0]['InternetGatewayId']