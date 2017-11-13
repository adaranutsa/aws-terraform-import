from python_terraform import *
import os
from glob import iglob

class Ec2:
    """Import AWS EC2 instances into terraform"""
    
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
        """Check for a base ec2_instance module configuration and
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
                    if 'module "ec2_instance"' in d:
                        
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
                f.write('\nmodule "ec2_instance" {\n')
                f.write('    source = "github.com/adaranutsa/tf_aws_ec2_instance"\n')
                f.write('}\n')
                
    def init(self):
        """Initialize the terraform resources"""
        
        self.tf.init(capture_output=False, no_color=IsNotFlagged)
        
    def get_ec2_instances(self):
        """Gather all EC2 instances to be imported into terraform"""
        
        ec2_instances = self.client.describe_instances()['Reservations']
        ec2_ids = []
        
        # Gather all EC2 ID's
        for ec2 in ec2_instances:
            for inst in ec2['Instances']:
                ec2_ids.append(inst['InstanceId'])
            
        return ec2_ids
        
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
            
    def import_ec2_instances(self):
        """Execute terraform import operations"""
        
        # Check to make sure configuration exists
        self.base_config()
        
        # Initialize terraform resources
        self.init()
        
        # Gather all ec2 resources
        ec2s = self.get_ec2_instances()
        
        # Import all resources
        self.import_resources('module.aws_instance.ec2_instance.id', ec2s)