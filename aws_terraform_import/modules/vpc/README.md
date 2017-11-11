# AWS Terraform Import - VPC Module

The VPC module imports VPC resources into a Terraform state file

### Resources Imported
The following resources are imported as of now

* All VPCs
* All Subnets
* All Route Tables that have subnet associations
* All Internet Gateways

### Dependencies
This module relies on a fork of the official Terraform VPC Module.

[Terraform VPC Module](https://github.com/adaranutsa/terraform-aws-vpc)

This means that all resources are imported into the following terraform configuration: `module "vpc"`
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
from aws_terraform_import.modules.vpc import Vpc

session = boto3.Session(profile_name="myprofile", region_name="us-east-1")

vpc = Vpc(session, cwd="/home/user/terraform/myproject")

# This method call will launch the process of importing
# all VPCs and their dependant resources. No other
# method calls need to be made.

vpc.import_vpcs()
```