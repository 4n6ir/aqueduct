# aqueduct

### Pre-Requisites

- https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2-linux.html

- https://github.com/victorskl/yawsso

### SSO Authentication

- https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-sso.html

### Installation

```
pip install aqueduct-utility
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
CDK Trust [ ]: 111111111111 
add -h or --help for usage help
```

### Help Menu

```
$ aqueduct --h
usage: aqueduct [-h] [--addacct] [--addreg] [--addtag] [--bootstrap]
                [--delacct] [--delreg] [--deltag] [--ssosetup]

aqueduct v0.0.3

optional arguments:
  -h, --help   show this help message and exit
  --addacct    Add Account
  --addreg     Add Region
  --addtag     Add Tag
  --bootstrap  Bootstrap CDK
  --delacct    Delete Account
  --delreg     Delete Region
  --deltag     Delete Tag
  --ssosetup   SSO Setup
```

### Add Account

```
$ aqueduct --addacct
Account Name [ ]: Pipeline
Account Number [ ]: 111111111111
```

### Add Region

```
$ aqueduct --addreg
Region [ ]: us-east-2
```

### Add Tag

```
$ aqueduct --addtag
tag i.e. key=value: 4n6ir=4n6ir
```

### Setup SSO Configuration

```
$ aqueduct --ssosetup
```

### Sync Legacy Credentials

```
$ yawsso
```

### Bootstrap CDK

```
$ aqueduct --bootstrap
CDK_NEW_BOOTSTRAP set, using new-style bootstrapping
 ⏳  Bootstrapping environment aws://111111111111/us-east-2...
Trusted accounts:   111111111111
Execution policies: arn:aws:iam::aws:policy/AdministratorAccess
cdk-bootstrap-4n6ir-111111111111-us-east-2: creating CloudFormation changeset...
[██████████████████████████████████████████████████████████] (11/11)








 ✅  Environment aws://111111111111/us-east-2 bootstrapped.
```
