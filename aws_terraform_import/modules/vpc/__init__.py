from python_terraform import *
import os
from glob import iglob
from .get_resources import GetResources
import json

class Vpc:
    """Import AWS VPC resources into terraform"""
    
    def __init__(self, session, cwd = os.getcwd()):
        """
        Initilize the class with the boto3 client and terraform wrapper
        
        :parameter session: boto3 session variabled. Required
        :type session: str
        :parameter cwd: Current working directory of the script. Optional.
        :type cwd: str
        
        If cwd is not specified, the current working directory
        of the script is used instead.
        """
        
        self.session = session
        self.client = session.client('ec2')
        self.cwd = cwd
           
        # Initialize the terraform class 
        self.tf = Terraform(working_dir=self.cwd)
        
    def base_config(self, num, vpc):
        """
        Check for a base vpc module configuration and
        create one if it doesn't exist.

        :parameter num: The number to indentify multiple VPCs
        :type num: int
        :parameter vpc: Boto3 VPC resource response
        :type vpc: dict
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
                    if 'module "vpc_{}"'.format(num) in d:

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
                f.write('\nmodule "vpc_{}"\n'.format(num))
                f.write('{\n')
                f.write('    source = "github.com/adaranutsa/terraform-aws-vpc"\n')
                f.write('name = "{}"\n'.format(vpc.name))
                f.write('cidr = "{}"\n'.format(vpc.cidr))
                f.write('azs = {}\n'.format(json.dumps(vpc.azs)))
                f.write('public_subnets = {}\n'.format(json.dumps(vpc.public_subnets)))
                f.write('enable_nat_gateway = {}\n'.format(str(vpc.enable_nat_gateway).lower()))
                #f.write('enable_vpn_gateway = {}\n'.format(str(vpc.enable_vpn_gateway).lower()))
                f.write('}\n')
    
    def init(self):
        """Initialize the terraform resources"""
        
        self.tf.init(capture_output=False, no_color=IsNotFlagged)
        
    
    def import_resources(self, module, resources):
        """
        Import resources into terraform
        
        :parameter module: The name of the terraform module this is being imported into
        :type module: str
        :parameter resources: List of resources to be imported
        :type resources: list
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
        
        # Gather all the resources
        resources = GetResources(self.session)
        vpcs = resources.get_vpcs()
        
        # Check to make sure configuration exists for each VPC
        count = 1
        
        # Create a VPC configuration for each VPC
        for vpc in vpcs:
            self.base_config(count, vpc)
            count += 1
        
        # Initialize terraform resources
        self.init()
        
        # Import all resources
        count = 1
        for vpc in vpcs:
            self.import_resources("module.vpc_{}.aws_vpc.this".format(count), [vpc.vpcid])
            self.import_resources("module.vpc_{}.aws_subnet.public".format(count), vpc.subnet_ids)
            self.import_resources("module.vpc_{}.aws_route_table.public".format(count), vpc.route_table_ids)
            self.import_resources("module.vpc_{}.aws_internet_gateway.this".format(count), [vpc.internet_gateway_id])
            
            count += 1
        
        # Format the terraform files
        self.tf.fmt(diff=False)