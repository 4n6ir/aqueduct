import aws_sso_lib
import boto3
import pathlib
import typer

def access(role,identity,region):

    roles = aws_sso_lib.list_available_roles(
        start_url = 'https://'+identity+'.awsapps.com/start',
        sso_region = region, 
        login = True
    )

    rolelist = []

    for account in roles:
        rolelist.append(account[2])

    unique = list(set(rolelist))

    if role not in unique:
        print('Role Access:')
        for item in unique:
            print(' * '+item)
        raise typer.Abort()

def accounts(selected_account,identity_store,sso_region):

    accounts = aws_sso_lib.list_available_accounts(
        start_url = 'https://'+identity_store+'.awsapps.com/start',
        sso_region = sso_region, 
        login = True
    )
    
    accountlist = []

    for account in accounts:
        accountlist.append(account[0])

    if selected_account not in accountlist:
        print('Account List:')
        for account in accountlist:
            print(' * '+account)
        raise typer.Abort()

def active(region):

    ec2_client = boto3.client('ec2')

    response = ec2_client.describe_regions()

    regionlist = []

    for regions in response['Regions']:
        regionlist.append(regions['RegionName'])

    if region not in regionlist:
        print('Active Regions:')
        for region in regionlist:
            print(' * '+region)
        raise typer.Abort()

def alias(selected_account,identity_store,sso_region):

    accounts = aws_sso_lib.list_available_accounts(
        start_url = 'https://'+identity_store+'.awsapps.com/start',
        sso_region = sso_region, 
        login = True
    )

    for account in accounts:
        if account[1].lower() == selected_account.lower():
            return account[0]

    raise typer.Abort()

def folders(folder):
    
    folderlist = []
    
    for path in pathlib.Path(pathlib.Path.cwd()).iterdir():
        if path.is_dir():
            folderlist.append(path.name)

    if folder not in folderlist:
        print('Folder List:')
        for folder in folderlist:
            print(' * '+folder)
        raise typer.Abort()

def outputs(output_format):

    output_formats = []
    output_formats.append('json')
    output_formats.append('yaml')
    output_formats.append('yaml-stream')
    output_formats.append('text')
    output_formats.append('table')

    if output_format not in output_formats:
        print('Output Formats:')
        for output in output_formats:
            print(' * '+output)
        raise typer.Abort()
