---


---

<h1 id="aws-terraform-import">AWS Terraform Import</h1>
<p>This tool will import existing AWS resources into Terraform state files and create a Terraform configuration for each of the resources being imported.</p>
<p>This project is still a work in progress. Please check back often for the latest updates.</p>
<h2 id="requirements">Requirements</h2>
<blockquote>
<p><strong>Note:</strong></p>
<ul>
<li>Python 2 is not supported</li>
<li>You will need to have the proper access to your AWS account prior to running this tool.</li>
</ul>
</blockquote>
<h3 id="tools">Tools</h3>
<ul>
<li><a href="https://www.python.org/downloads/">python3</a> - Only Python3 is supported with this package</li>
<li><a href="https://pypi.python.org/pypi/python-terraform/0.9.1">python_terraform</a> - Python terraform wrapper</li>
<li><a href="http://boto3.readthedocs.io/en/latest/guide/quickstart.html#installation">boto3</a> - Boto3 for communicating with AWS to retrieve resources</li>
<li><a href="https://www.terraform.io/">terraform</a> - Terraform for managing the infrastructure</li>
</ul>

