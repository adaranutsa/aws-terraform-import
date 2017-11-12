# AWS Terraform Import - VPC Module

The EC2 module imports EC2 resources into a Terraform state file

### Resources Imported
The following resources are imported as of now

* EC2 instances

### Dependencies
This module relies on a fork of the official Terraform EC2 Instance Module.

[Terraform EC2 Instance Module](https://github.com/adaranutsa/tf_aws_ec2_instance)

This means that all resources are imported into the following terraform configuration: `module "ec2_instance"`
This module will check if that configuration exists in your terraform directory and if not, it will
create it and append it to `main.tf` terraform file.

### Module Usage
This module is intended to be used by the package. However, it can be used independantly as well
if you so choose. See below for usage instructions.

The modules requires that a boto3 session be created and passed to the Vpc class.
The Vpc class also takes an optional current working directory parameter for
specifying your terraform working directory. If one is not passed, it uses the
script's current directory for terraform. So be careful and pass one if needed.

Example code:
```python
import boto3
from aws_terraform_import.modules.ec2 import Ec2

session = boto3.Session(profile_name="myprofile", region_name="us-east-1")

ec2 = Ec2(session, cwd="/home/user/terraform/myproject")

# This method call will launch the process of importing
# all VPCs and their dependant resources. No other
# method calls need to be made.

ec2.import_ec2_instances()
```