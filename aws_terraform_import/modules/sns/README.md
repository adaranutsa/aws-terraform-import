# AWS Terraform Import - SNS Module

The SNS module imports SNS resources into a Terraform state file

### Resources Imported
The following resources are imported as of now

* All SNS Topics

### Dependencies
This module relies on the official Terraform VPC Module.

[Terraform SNS Module](https://github.com/terraform-community-modules/tf_aws_sns)

This means that each SNS Topic is imported into the following terraform configurations: `module "sns_<topic name>"`
This module will check if that configurations exist in your terraform directory and if not, it will create them and append to `main.tf` terraform file.

### Module Usage
This module is intended to be used by the package. However, it can be used independantly as well
if you so choose. See below for usage instructions.

The modules requires that a boto3 session be created and passed to the Sns class.
The Sns class also takes an optional current working directory parameter for
specifying your terraform working directory. If one is not passed, it uses the
script's current directory for terraform. So be careful and pass one if needed.

Example code:
```python
import boto3
from aws_terraform_import.modules.sns import Sns

session = boto3.Session(profile_name="myprofile", region_name="us-east-1")

sns = Sns(session, cwd="/home/user/terraform/myproject")

# This method call will launch the process of importing
# all SNS Topic. No other method calls need to be made.

sns.import_sns()
```
