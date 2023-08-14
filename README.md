# aqueduct

### Installation

<details>
<summary>Requirement</summary>

AWS Command Line Interface (AWS CLI) Version 2

```
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
aws --version
```

https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html

</details>

<details>
<summary>Deployment</summary>

```
pip install aqueduct-utility
```

</details>

<details>
<summary>Shell Completion</summary>

```
aqueduct --install-completion
```

</details>

### IAM Identity Center 

<details>
<summary>Single Sign-On</summary>

```
$ aqueduct login
Identity Store: portal
SSO Region: us-east-2
SSO Role: AWSAdministratorAccess
CLI Region: us-east-2
CLI Output: json
Authenticated!!
```

</details>

<details>
<summary>Single Sign-Out</summary>

```
$ aqueduct logout 
Logged Out!!
```

</details>

### Deployment

<details>
<summary>All Accounts</summary>

```
$ aqueduct deploy
Deploy Folder: test
Deploy [y/N]: y
--------------------------------------
Deploy AccountName 123456789012
--------------------------------------

✨  Synthesis time: 10.9s

TestStack: building assets...

[0%] start: Building 93a9449a1ac92f796d777916aae26c4c0e5740a72635c27014a56be5bcd35e4d:123456789012-us-east-2
[100%] success: Built 93a9449a1ac92f796d777916aae26c4c0e5740a72635c27014a56be5bcd35e4d:123456789012-us-east-2

TestStack: assets built

TestStack: deploying...
[0%] start: Publishing 93a9449a1ac92f796d777916aae26c4c0e5740a72635c27014a56be5bcd35e4d:123456789012-us-east-2
[100%] success: Published 93a9449a1ac92f796d777916aae26c4c0e5740a72635c27014a56be5bcd35e4d:123456789012-us-east-2
TestStack: creating CloudFormation changeset...

 ✅  TestStack

✨  Deployment time: 16.51s

Stack ARN:
arn:aws:cloudformation:us-east-2:123456789012:stack/TestStack/58a84490-6931-11ed-ab5a-0a2c7b97f37e

✨  Total time: 27.41s

```

</details>

### Destruction

<details>
<summary>All Accounts</summary>

```
$ aqueduct destroy
Destroy Folder: test
Destroy [y/N]: y
--------------------------------------
Destroy AccountName 123456789012
--------------------------------------
TestStack: destroying...

 ✅  TestStack: destroyed

```

</details>

### Hints

<details>
<summary>Common Commands</summary>

```
$ aqueduct hints

** INSTALLATION **

npm install -g aws-cdk
npm install -g npm@9.6.7
npm install -g node@18.0.0 --force

** APPLICATION **

cdk init app --language python
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt --upgrade

** GITIGNORE **

echo .~c9* > ~/.gitignore
echo cdk.context.json >> ~/.gitignore
git config --global core.excludesfile ~/.gitignore
```

</details>

### Suppression

<details>
<summary>Code Generation</summary>

https://constructs.dev/packages/cdk-nag

```
$ aqueduct nag
{"id":"AwsSolutions-IAM4","reason":"The IAM user, role, or group uses AWS managed policies."},
```

</details>

### Validation

<details>
<summary>Items Checked</summary>


 - Deploy Folder
 - Destroy Folder
 - Output Format

</details>

### Development

<details>
<summary>Local Build</summary>

```
python setup.py install --user
```

</details>
