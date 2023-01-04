import aws_sso_lib
import pathlib
import typer
import aqueduct.validation as _valid

def login():

    identity = pathlib.Path.joinpath(pathlib.Path.home(),'.aqueduct_idp')
    sso = pathlib.Path.joinpath(pathlib.Path.home(),'.aqueduct_sso')
    role = pathlib.Path.joinpath(pathlib.Path.home(),'.aqueduct_role')
    cli = pathlib.Path.joinpath(pathlib.Path.home(),'.aqueduct_cli')
    output = pathlib.Path.joinpath(pathlib.Path.home(),'.aqueduct_output')
    trust = pathlib.Path.joinpath(pathlib.Path.home(),'.aqueduct_trust')
    regions = pathlib.Path.joinpath(pathlib.Path.home(),'.aqueduct_regions')

### identity ###

    if identity.is_file() == False:

        identity_store = typer.prompt("Identity Store").strip()
        pathlib.Path(identity).write_text(identity_store)

    else:

        identity_store = pathlib.Path(identity).read_text()
        correct = typer.confirm("Identity Store {"+identity_store+"}")

        if not correct:

            identity_store = typer.prompt("Identity Store").strip()
            pathlib.Path(identity).write_text(identity_store)

### sso region ###

    if sso.is_file() == False:

        sso_region = typer.prompt("SSO Region").strip()
        _valid.active(sso_region)
        pathlib.Path(sso).write_text(sso_region)

    else:

        sso_region = pathlib.Path(sso).read_text()
        correct = typer.confirm("SSO Region {"+sso_region+"}")

        if not correct:

            sso_region = typer.prompt("SSO Region").strip()
            _valid.active(sso_region)
            pathlib.Path(sso).write_text(sso_region)

### sso login ###

    login = aws_sso_lib.login(
        start_url = 'https://'+identity_store+'.awsapps.com/start',
        sso_region = sso_region, 
        disable_browser = True
    )

### sso role ###

    if role.is_file() == False:

        sso_role = typer.prompt("SSO Role").strip()
        _valid.access(sso_role, identity_store, sso_region)
        pathlib.Path(role).write_text(sso_role)

    else:

        sso_role = pathlib.Path(role).read_text()
        correct = typer.confirm("SSO Role {"+sso_role+"}")

        if not correct:

            sso_role = typer.prompt("SSO Role").strip()
            _valid.access(sso_role, identity_store, sso_region)
            pathlib.Path(role).write_text(sso_role)

### cli region ###

    if cli.is_file() == False:

        cli_region = typer.prompt("CLI Region").strip()
        _valid.active(cli_region)
        pathlib.Path(cli).write_text(cli_region)

    else:

        cli_region = pathlib.Path(cli).read_text()
        correct = typer.confirm("CLI Region {"+cli_region+"}")

        if not correct:

            cli_region = typer.prompt("CLI Region").strip()
            _valid.active(cli_region)
            pathlib.Path(cli).write_text(cli_region)

### cli output ###

    if output.is_file() == False:

        cli_output = typer.prompt("CLI Output").strip()
        _valid.outputs(cli_output)
        pathlib.Path(output).write_text(cli_output)

    else:

        cli_output = pathlib.Path(output).read_text()
        correct = typer.confirm("CLI Output {"+cli_output+"}")

        if not correct:

            cli_output = typer.prompt("CLI Output").strip()
            _valid.outputs(cli_output)
            pathlib.Path(output).write_text(cli_output)

### cdk trust ###

    if trust.is_file() == False:

        cdk_trust = typer.prompt("CDK Trust").strip()
        if len(cdk_trust) == 12 and cdk_trust.isdigit():
            _valid.accounts(cdk_trust,identity_store,sso_region)
        else:
            cdk_trust = _valid.alias(cdk_trust,identity_store,sso_region)
        pathlib.Path(trust).write_text(cdk_trust)

    else:

        cdk_trust = pathlib.Path(trust).read_text()
        correct = typer.confirm("CDK Trust {"+cdk_trust+"}")

        if not correct:

            cdk_trust = typer.prompt("CDK Trust").strip()
            if len(cdk_trust) == 12 and cdk_trust.isdigit():
                _valid.accounts(cdk_trust,identity_store,sso_region)
            else:
                cdk_trust = _valid.alias(cdk_trust,identity_store,sso_region)
            pathlib.Path(trust).write_text(cdk_trust)

### cdk regions ###

    if regions.is_file() == False:

        cdk_regions = typer.prompt("CDK Regions").strip()
        try:
            parsed = cdk_regions.split('|')
            for parse in parsed:
                _valid.active(parse)
            pathlib.Path(regions).write_text(cdk_regions)
        except:
            raise typer.Abort()

    else:

        cdk_regions = pathlib.Path(regions).read_text()
        correct = typer.confirm("CDK Regions {"+cdk_regions+"}")

        if not correct:

            cdk_regions = typer.prompt("CDK Regions").strip()
            try:
                parsed = cdk_regions.split('|')
                for parse in parsed:
                    _valid.active(parse)
                pathlib.Path(regions).write_text(cdk_regions)
            except:
                raise typer.Abort()

### configuration ###
    
    config = pathlib.Path.joinpath(pathlib.Path.home(),'.aws','config')
    pathlib.Path(config).parents[0].mkdir(parents = True, exist_ok = True)
    
    accounts = aws_sso_lib.list_available_accounts(
        start_url = 'https://'+identity_store+'.awsapps.com/start',
        sso_region = sso_region, 
        login = True
    )

    f = pathlib.Path(config).open('w')

    for account in accounts:
        
        alias = account[1].replace(' ','')

        f.write('[profile '+alias+']\n')
        f.write('credential_process = aws-sso-util credential-process --profile '+alias+'\n')
        f.write('sso_start_url = https://'+identity_store+'.awsapps.com/start\n')    
        f.write('sso_region = '+sso_region+'\n')
        f.write('sso_account_id = '+account[0]+'\n')
        f.write('sso_role_name = '+sso_role+'\n')
        f.write('region = '+cli_region+'\n')
        f.write('output = '+cli_output+'\n\n')

    f.close()

    print('Authenticated!!')

def logout():

    identity = pathlib.Path.joinpath(pathlib.Path.home(),'.aqueduct_idp')
    identity_store = pathlib.Path(identity).read_text()

    sso = pathlib.Path.joinpath(pathlib.Path.home(),'.aqueduct_sso')
    sso_region = pathlib.Path(sso).read_text()

    aws_sso_lib.sso.logout(
        start_url = 'https://'+identity_store+'.awsapps.com/start',
        sso_region = sso_region,
        sso_cache = None
    )

    print('Logged Out!!')
