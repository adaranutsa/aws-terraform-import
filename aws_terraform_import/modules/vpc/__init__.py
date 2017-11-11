from python_terraform import *
import os
from glob import iglob

class Vpc:
    """Import AWS VPC resources into terraform"""
    
    def __init__(self, session, cwd = None):
        """Initilize the class with the boto3 client and terraform wrapper
        
           session: boto3 session variabled. Required
           cwd: Current working directory of the script. Optional.
           
           If cwd is not specified, the current working directory
           of the script is used instead.
        """
        
        # Create the boto3 client
        self.client = session.client('ec2')
        
        # If no cwd is specified, use current dir of script
        if cwd == None:
            self.cwd = os.getcwd()
        else:
            self.cwd = cwd
           
        # Initialize the terraform class 
        self.tf = Terraform(working_dir=self.cwd)
        
    def base_config(self):
        """Check for a base vpc module configuration and
        create one if it doesn't exist.
        """
        
        # Get a list of all .tf files
        configs = iglob("{}/*.tf".format(self.cwd), recursive=False)
        
        # Store whether the config file for module vpc exists
        config_exists = False
        
        # Loop the tf config files
        for config in configs:
            
            # Open each config file
            with open(config, 'r') as f:
                
                # Read config file lines
                data = f.readlines()
                
                # Loop each config file line
                for d in data:
                    
                    # Check if the vpc module exists
                    if 'module "vpc"' in d:
                        
                        # If the config exists, change the config_exists flag
                        # to True and break out of the loop
                        config_exists = True
                        break
            
            # If the config was found, break the loop
            # so as not to waste time searching files
            if config_exists:
                break
            
        # If the config file doesn't exist, append the
        # config to the main.tf file
        if not config_exists:
            
            # Append the config to the main.tf file
            with open("{}/main.tf".format(self.cwd), 'a') as f:
                f.write('\nmodule "vpc" {\n')
                f.write('    source = "github.com/adaranutsa/terraform-aws-vpc"\n')
                f.write('}\n')
    
    def init(self):
        """Initialize the terraform resources"""
        
        self.tf.init(capture_output=False, no_color=IsNotFlagged)
        
    def get_vpcs(self):
        """Gather all VPCs to be imported into terraform"""
        
        vpcs = self.client.describe_vpcs()
        vpc_ids = []
        
        # Gather all the VPC ID's
        for vpc in vpcs['Vpcs']:
            vpc_ids.append(vpc['VpcId'])
            
        return vpc_ids
            
    def get_subnets(self):
        """Gather all Subnets to be imported into terraform"""
        
        subnets = self.client.describe_subnets()
        subnet_ids = []
        
        # Gather all the subnet ID's
        for subnet in subnets['Subnets']:
            subnet_ids.append(subnet['SubnetId'])
            
        return subnet_ids
            
    def get_route_tables(self):
        """Gather all route tables to be imported into terraform"""
        
        route_tables = self.client.describe_route_tables()
        route_table_ids = []
        
        # Gather all route table ID's
        for rt in route_tables['RouteTables']:
            
            if 'SubnetId' not in rt['Associations'][0]:
                # This route table has no subnet associations, ignore it
                continue
            
            route_table_ids.append(rt['RouteTableId'])
        
        return route_table_ids
            
    def get_internet_gateways(self):
        """Gather all internet gateways to be imported into terraform"""
        
        internet_gateways = self.client.describe_internet_gateways()
        internet_gateway_ids = []
        
        # Gather all the gateway ID's        
        for igw in internet_gateways['InternetGateways']:
            internet_gateway_ids.append(igw['InternetGatewayId'])
            
        return internet_gateway_ids
    
    def import_resources(self, module, resources):
        """Import resources into terraform
        
           module: The terraform module this is being imported into
           resources: List of resources to be imported
        """
        
        # Count name for keeping track of the number of 
        # resources being imported
        count = 0
        length = len(resources)
        
        # If the resource list if empty, return message
        if length == 0:
            return "No resources available to import"
           
        # Loop the resources to be imported 
        for res in resources:
            
            # If there's only one resource to import, import it
            if length == 1:
                self.tf.import_cmd(module, res, capture_output=False, no_color=IsNotFlagged)
                
            # If there are multiple resources to import, number
            # the imports using the 'count' name
            else:
                mod = "{}[{}]".format(module, count)
                self.tf.import_cmd(mod, res, capture_output=False, no_color=IsNotFlagged)
            
            # Increment the coutner
            count += 1
    
    def import_vpcs(self):
        """Execute terraform import operations"""
        
        # Check to make sure configuration exists
        self.base_config()
        
        # Initialize terraform resources
        self.init()
        
        # Gather all the resources
        vpcs = self.get_vpcs()
        subnets = self.get_subnets()
        route_tables = self.get_route_tables()
        internet_gateways = self.get_internet_gateways()
        
        # Import all resources
        self.import_resources("module.vpc.aws_vpc.this", vpcs)
        self.import_resources("module.vpc.aws_subnet.public", subnets)
        self.import_resources("module.vpc.aws_route_table.public", route_tables)
        self.import_resources("module.vpc.aws_internet_gateway.this", internet_gateways)
        
        
        