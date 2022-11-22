import aws_sso_lib
import os
import pathlib
import typer
import aqueduct.validation as _valid

def deploy():
    
    deploy_folder = typer.prompt("Deploy Folder").strip()
    _valid.folders(deploy_folder)

    confirm = typer.confirm("Deploy")

    if not confirm:

        raise typer.Abort()

    if pathlib.Path.joinpath(pathlib.Path.cwd(),deploy_folder,'.venv').exists() == False:
        os.system('cd '+deploy_folder+' && python3 -m venv .venv')
        os.system('cd '+deploy_folder+' && source .venv/bin/activate && pip3 install -r requirements.txt --upgrade')

    identity = pathlib.Path.joinpath(pathlib.Path.home(),'.aqueduct_idp')
    identity_store = pathlib.Path(identity).read_text()

    sso = pathlib.Path.joinpath(pathlib.Path.home(),'.aqueduct_sso')
    sso_region = pathlib.Path(sso).read_text()

    accounts = aws_sso_lib.list_available_accounts(
        start_url = 'https://'+identity_store+'.awsapps.com/start',
        sso_region = sso_region, 
        login = True
    )

    for account in accounts:

        print('--------------------------------------')
        print('Deploy '+account[1]+' '+str(account[0]))
        print('--------------------------------------')

        alias = account[1].replace(' ','')

        os.system('cd '+deploy_folder+' && source .venv/bin/activate && cdk deploy --profile '+alias+' --all --require-approval never')
