import aws_sso_lib
import boto3
import json
import os
import pathlib
import time
import typer
import aqueduct.validation as _valid

app = typer.Typer()

def action(task):

    action_folder = typer.prompt(task+" Folder").strip()
    _valid.folders(action_folder)

    confirm = typer.confirm(task)

    if not confirm:

        raise typer.Abort()

    identity = pathlib.Path.joinpath(pathlib.Path.home(),'.aqueduct_idp')
    identity_store = pathlib.Path(identity).read_text()

    sso = pathlib.Path.joinpath(pathlib.Path.home(),'.aqueduct_sso')
    sso_region = pathlib.Path(sso).read_text()

    trust = pathlib.Path.joinpath(pathlib.Path.home(),'.aqueduct_trust')
    cdk_trust = pathlib.Path(trust).read_text()

    regions = pathlib.Path.joinpath(pathlib.Path.home(),'.aqueduct_regions')
    cdk_regions = pathlib.Path(regions).read_text()

    regionlist = cdk_regions.split('|')

    accounts = aws_sso_lib.list_available_accounts(
        start_url = 'https://'+identity_store+'.awsapps.com/start',
        sso_region = sso_region, 
        login = True
    )

    lambda_client = boto3.client('lambda')
    s3_client = boto3.client('s3')

    conduit_name = 'conduit-nanopipeline-'+str(cdk_trust)+'-'+sso_region

    for account in accounts:
        for region in regionlist:

            print('--------------------------------------')
            print(task+' '+account[1]+' '+region)
            print('--------------------------------------')

            alias = account[1].replace(' ','')

            package_name = alias+'-'+action_folder

            os.system('cp -R '+action_folder+' '+package_name)

            f = open(package_name+'/app.py', 'r')
            data = f.read()
            data = data.replace("os.getenv('CDK_DEFAULT_ACCOUNT')", "'"+str(account[0])+"'")
            data = data.replace("os.getenv('CDK_DEFAULT_REGION')", "'"+region+"'")
            f.close()

            f = open(package_name+'/app.py', 'w')
            f.write(data)
            f.close()            

            os.system('zip -r '+package_name+'.zip '+package_name)

            s3_client.upload_file(package_name+'.zip', conduit_name, package_name+'.zip')

            bundle = {}
            bundle['bundle'] = package_name+'.zip'
            bundle['type'] = task.lower()

            lambda_client.invoke(
                FunctionName = conduit_name,
                InvocationType = 'Event',
                Payload = json.dumps(bundle)
            )

            time.sleep(1)

            os.system('rm -rf '+package_name)
            os.system('rm '+package_name+'.zip')

@app.command()
def deploy():
    action('Deploy')

@app.command()
def destroy():
    action('Destroy')

if __name__ == "__main__":
    app()
