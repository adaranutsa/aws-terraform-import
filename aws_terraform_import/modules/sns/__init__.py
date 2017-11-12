from python_terraform import *
import os


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

    def base_config(self):
        """Create main.tf config file if it does not exist"""

        open('{}/main.tf'.format(self.cwd), 'a').close()

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

    def append_sns_topic(self, name):
        """Append topics to main.tf
           name var is a requirement for SNS module,
           therefore adding each topic as a separate config to main.tf with name
        """

        with open('{}/main.tf'.format(self.cwd), 'a') as f:
            f.write('module "sns_%s" {\n' % name)
            f.write('source ="github.com/terraform-community-modules/tf_aws_sns"\n')
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

        # Create base file
        self.base_config()

        # Create base config for each SNS Topic
        for arn in arns:
            self.append_sns_topic(self.get_sns_name(arn))

        # Initialize terraform resources
        self.init()

        # Import all resources
        for arn in arns:
            self.import_resources("module.sns_{}.aws_sns_topic.t".format(self.get_sns_name(arn)), arn)


