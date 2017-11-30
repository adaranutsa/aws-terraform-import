<!DOCTYPE html>
<html>

<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>README</title>
  <link rel="stylesheet" href="https://stackedit.io/style.css" />
</head>

<body class="stackedit">
  <div class="stackedit__left">
    <div class="stackedit__toc">
      
<ul>
<li><a href="#aws-terraform-import">AWS Terraform Import</a>
<ul>
<li><a href="#requirements">Requirements</a></li>
<li><a href="#current-relationship">Current relationship</a></li>
</ul>
</li>
</ul>

    </div>
  </div>
  <div class="stackedit__right">
    <div class="stackedit__html">
      <h1 id="aws-terraform-import">AWS Terraform Import</h1>
<p>This tool will import existing AWS resources into Terraform state files and create a Terraform configuration for each of the resources being imported.</p>
<p>This project is still a work in progress.</p>
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
<h2 id="current-relationship">Current relationship</h2>
<div class="mermaid"><svg xmlns="http://www.w3.org/2000/svg" id="mermaid-svg-EIbUtZE8roLS2JWb" height="100%" viewBox="0 0 375.359375 202" style="max-width:375.359375px;"><g><g class="output"><g class="clusters"></g><g class="edgePaths"><g class="edgePath" style="opacity: 1;"><path class="path" d="M84.14290364583333,58L115.53125,33L153.34375,38.4473832301632" marker-end="url(#arrowhead1704)" style="fill:none"></path><defs><marker id="arrowhead1704" viewBox="0 0 10 10" refX="9" refY="5" markerUnits="strokeWidth" markerWidth="8" markerHeight="6" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" class="arrowheadPath" style="stroke-width: 1; stroke-dasharray: 1, 0;"></path></marker></defs></g><g class="edgePath" style="opacity: 1;"><path class="path" d="M216.546875,43L254.359375,43L279.359375,43" marker-end="url(#arrowhead1705)" style="fill:none"></path><defs><marker id="arrowhead1705" viewBox="0 0 10 10" refX="9" refY="5" markerUnits="strokeWidth" markerWidth="8" markerHeight="6" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" class="arrowheadPath" style="stroke-width: 1; stroke-dasharray: 1, 0;"></path></marker></defs></g><g class="edgePath" style="opacity: 1;"><path class="path" d="M153.34375,60.299943725379855L115.53125,81L90.53125,81" marker-end="url(#arrowhead1706)" style="fill:none"></path><defs><marker id="arrowhead1706" viewBox="0 0 10 10" refX="9" refY="5" markerUnits="strokeWidth" markerWidth="8" markerHeight="6" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" class="arrowheadPath" style="stroke-width: 1; stroke-dasharray: 1, 0;"></path></marker></defs></g><g class="edgePath" style="opacity: 1;"><path class="path" d="M79.1640625,104L115.53125,139L140.53125,139" marker-end="url(#arrowhead1707)" style="fill:none"></path><defs><marker id="arrowhead1707" viewBox="0 0 10 10" refX="9" refY="5" markerUnits="strokeWidth" markerWidth="8" markerHeight="6" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" class="arrowheadPath" style="stroke-width: 1; stroke-dasharray: 1, 0;"></path></marker></defs></g></g><g class="edgeLabels"><g class="edgeLabel" transform="" style="opacity: 1;"><g transform="translate(0,0)" class="label"><foreignObject width="0" height="0"><div xmlns="http://www.w3.org/1999/xhtml" style="display: inline-block; white-space: nowrap;"><span class="edgeLabel"></span></div></foreignObject></g></g><g class="edgeLabel" transform="" style="opacity: 1;"><g transform="translate(0,0)" class="label"><foreignObject width="0" height="0"><div xmlns="http://www.w3.org/1999/xhtml" style="display: inline-block; white-space: nowrap;"><span class="edgeLabel"></span></div></foreignObject></g></g><g class="edgeLabel" transform="" style="opacity: 1;"><g transform="translate(0,0)" class="label"><foreignObject width="0" height="0"><div xmlns="http://www.w3.org/1999/xhtml" style="display: inline-block; white-space: nowrap;"><span class="edgeLabel"></span></div></foreignObject></g></g><g class="edgeLabel" transform="" style="opacity: 1;"><g transform="translate(0,0)" class="label"><foreignObject width="0" height="0"><div xmlns="http://www.w3.org/1999/xhtml" style="display: inline-block; white-space: nowrap;"><span class="edgeLabel"></span></div></foreignObject></g></g></g><g class="nodes"><g class="node" id="A" transform="translate(55.265625,81)" style="opacity: 1;"><rect rx="0" ry="0" x="-35.265625" y="-23" width="70.53125" height="46"></rect><g class="label" transform="translate(0,0)"><g transform="translate(-25.265625,-13)"><foreignObject width="50.53125" height="26"><div xmlns="http://www.w3.org/1999/xhtml" style="display: inline-block; white-space: nowrap;">Python</div></foreignObject></g></g></g><g class="node" id="B" transform="translate(184.9453125,43)" style="opacity: 1;"><rect rx="0" ry="0" x="-31.6015625" y="-23" width="63.203125" height="46"></rect><g class="label" transform="translate(0,0)"><g transform="translate(-21.6015625,-13)"><foreignObject width="43.203125" height="26"><div xmlns="http://www.w3.org/1999/xhtml" style="display: inline-block; white-space: nowrap;">Boto3</div></foreignObject></g></g></g><g class="node" id="C" transform="translate(307.359375,43)" style="opacity: 1;"><rect rx="0" ry="0" x="-28" y="-23" width="56" height="46"></rect><g class="label" transform="translate(0,0)"><g transform="translate(-18,-13)"><foreignObject width="36" height="26"><div xmlns="http://www.w3.org/1999/xhtml" style="display: inline-block; white-space: nowrap;">AWS</div></foreignObject></g></g></g><g class="node" id="D" transform="translate(184.9453125,139)" style="opacity: 1;"><rect rx="5" ry="5" x="-44.4140625" y="-23" width="88.828125" height="46"></rect><g class="label" transform="translate(0,0)"><g transform="translate(-34.4140625,-13)"><foreignObject width="68.828125" height="26"><div xmlns="http://www.w3.org/1999/xhtml" style="display: inline-block; white-space: nowrap;">Terraform</div></foreignObject></g></g></g></g></g></g></svg></div>

    </div>
  </div>
</body>

</html>
