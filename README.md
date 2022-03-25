# aqueduct

### Permissions

I recommend using an AWS Account with Delegated Administration from Firewall Manager, Guard Duty, Stack Sets, etc., to access the required Organization permission.

 - ec2:DescribeRegions
 - organizations:ListAccounts

### Requirements

- https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html

```
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
aws --version
```

- https://github.com/benkehoe/aws-sso-util

```
pip3 install aws-sso-util
```

### Installation

```
pip3 install aqueduct-utility
```

### Initial Configuration

```
$ aqueduct 
SSO Start URL [ ]: https://portal.awsapps.com/start
SSO Region [ ]: us-east-2
SSO Role [AWSAdministratorAccess]: 
CLI Region [ ]: us-east-2
CLI Output [json]:     
CDK Qualifier [ ]: 4n6ir
```

### Aqueduct Menu

```
--------------------------------
AQUEDUCT v0.8.2
--------------------------------
  Bootstrap
  Command
  Configure
  Deploy
  Destroy
> Nanopipeline
  Presets
  Quit
```

### Conduit Micropipeline

 - https://github.com/4n6ir/conduit

Permissions

 - lambda:InvokeFunction
 - s3:PutObject

### Local Development

```
$ python setup.py install --user
```
