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
CDK Trust: 123456789012
CDK Regions: us-east-1|us-east-2
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
npm install -g aws-cdk
cdk init app --language python
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt --upgrade
echo .~c9* > ~/.gitignore
echo cdk.context.json >> ~/.gitignore
git config --global core.excludesfile ~/.gitignore
git checkout -b dev
```

</details>

### Nanopipeline

<details>
<summary>Deploy</summary>

Permissions: ```lambda:InvokeFunction``` & ```s3:PutObject```

```
$ aqueduct nanopipeline deploy
Deploy Folder: test
Deploy [y/N]: y
--------------------------------------
Deploy AccountName us-east-1
--------------------------------------
  adding: AccountName-test/ (stored 0%)
  adding: AccountName-test/test/ (stored 0%)
  adding: AccountName-test/test/test_stack.py (deflated 45%)
  adding: AccountName-test/test/__init__.py (stored 0%)
  adding: AccountName-test/test/__pycache__/ (stored 0%)
  adding: AccountName-test/test/__pycache__/__init__.cpython-37.pyc (deflated 26%)
  adding: AccountName-test/test/__pycache__/test_stack.cpython-37.pyc (deflated 35%)
  adding: AccountName-test/.gitignore (deflated 16%)
  adding: AccountName-test/README.md (deflated 54%)
  adding: AccountName-test/app.py (deflated 37%)
  adding: AccountName-test/cdk.json (deflated 56%)
  adding: AccountName-test/requirements-dev.txt (stored 0%)
  adding: AccountName-test/requirements.txt (deflated 4%)
  adding: AccountName-test/source.bat (deflated 43%)
  adding: AccountName-test/tests/ (stored 0%)
  adding: AccountName-test/tests/__init__.py (stored 0%)
  adding: AccountName-test/tests/unit/ (stored 0%)
  adding: AccountName-test/tests/unit/__init__.py (stored 0%)
  adding: AccountName-test/tests/unit/test_test_stack.py (deflated 42%)
```

</details>

<details>
<summary>Destroy</summary>

Permissions: ```lambda:InvokeFunction``` & ```s3:PutObject```

```
$ aqueduct nanopipeline destroy
Destroy Folder: test
Destroy [y/N]: y
--------------------------------------
Destroy AccountName us-east-1
--------------------------------------
  adding: AccountName-test/ (stored 0%)
  adding: AccountName-test/test/ (stored 0%)
  adding: AccountName-test/test/test_stack.py (deflated 45%)
  adding: AccountName-test/test/__init__.py (stored 0%)
  adding: AccountName-test/test/__pycache__/ (stored 0%)
  adding: AccountName-test/test/__pycache__/__init__.cpython-37.pyc (deflated 26%)
  adding: AccountName-test/test/__pycache__/test_stack.cpython-37.pyc (deflated 35%)
  adding: AccountName-test/.gitignore (deflated 16%)
  adding: AccountName-test/README.md (deflated 54%)
  adding: AccountName-test/app.py (deflated 37%)
  adding: AccountName-test/cdk.json (deflated 56%)
  adding: AccountName-test/requirements-dev.txt (stored 0%)
  adding: AccountName-test/requirements.txt (deflated 4%)
  adding: AccountName-test/source.bat (deflated 43%)
  adding: AccountName-test/tests/ (stored 0%)
  adding: AccountName-test/tests/__init__.py (stored 0%)
  adding: AccountName-test/tests/unit/ (stored 0%)
  adding: AccountName-test/tests/unit/__init__.py (stored 0%)
  adding: AccountName-test/tests/unit/test_test_stack.py (deflated 42%)
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

 - CLI Output Format
 - Deploy Folder
 - Destroy Folder
 - SSO Active Region
 - SSO Active Role

</details>

### Development

<details>
<summary>Local Build</summary>

```
python setup.py install --user
```

</details>
