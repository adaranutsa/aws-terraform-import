from python_terraform import *
import os
from glob import iglob


class Sns:
    """Import AWS SNS Topics into terraform"""

    def __init__(self, session, cwd = None):
        """Initialize the class with the boto3 client and terraform wrapper

           session: boto3 session variables. Required
           cwd: Current working directory of the script. Optional.

           If cwd is not specified, the current working directory
           of the script is used instead.
        """

        # Create the boto3 client
        self.client = session.client('sns')

        # If no cwd is specified, use current dir of script
        if cwd == None:
            self.cwd = os.getcwd()
        else:
            self.cwd = cwd

        # Initialize the terraform class
        self.tf = Terraform(working_dir=self.cwd)

    def get_sns_name(self, arn):
        """Get the SNS name from ARN
           Terraform does not have an easy way of retrieving the name
        """
        # Get the index of the last :
        separator_index = arn.rindex(':') + 1

        # Return everything to the right of last : (topic name)
        return arn[separator_index:]

    def init(self):
        """Initialize the terraform resources"""

        self.tf.init(capture_output=False, no_color=IsNotFlagged)

    def base_config(self, name):
        """Append topics to main.tf
           name var is a requirement for SNS module,
           therefore adding each topic as a separate config to main.tf with name
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
                    if 'module "sns_{}"'.format(name) in d:

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

            with open('{}/main.tf'.format(self.cwd), 'a') as f:
                f.write('module "sns_{}" '.format(name))
                f.write('{\n')
                f.write('source ="github.com/adaranutsa/tf_aws_sns"\n')
                f.write('name="{}"\n'.format(name))
                f.write('}')

    def get_sns_arns(self):
        """Gather all SNS topics to be imported in terraform"""

        arns = []

        # Gather all SNS Topic ARNs
        for topic in self.client.list_topics()['Topics']:
            arns.append(topic['TopicArn'])

        return arns

    def import_resources(self, module, resource):
        """Import resources into terraform

           module: The terraform module this is being imported into
           resources: List of resources to be imported
        """

        # Number of resources to be imported
        length = len(resource)

        # If the resource list if empty, return message
        if length == 0:
            return "No resources available to import"

        self.tf.import_cmd(module, resource, capture_output=False, no_color=IsNotFlagged)

    def import_sns(self):
        """Execute terraform import operations"""

        # Gather all resources
        arns = self.get_sns_arns()

        # Create base config for each SNS Topic
        for arn in arns:
            self.base_config(self.get_sns_name(arn))

        # Initialize terraform resources
        self.init()

        # Import all resources
        for arn in arns:
            self.import_resources("module.sns_{}.aws_sns_topic.t".format(self.get_sns_name(arn)), arn)

