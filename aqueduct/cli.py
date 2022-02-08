import boto3
import json
import os
import sys
import time
from aqueduct import __version__
from simple_term_menu import TerminalMenu
from subprocess import run

### ANSWER MAIN MENU OPTIONS ###

def action(menu, path, sso):
    if menu == "Bootstrap":
        print(' ')
        print('Bootstrapping...')
        print(' ')
        bootstrap(path)
    elif menu == "Command":
        print(' ')
        print('Command Line...')
        print(' ')
        command(path)
    elif menu == "Configure":
        print(' ')
        print('Configuring...')
        print(' ')
        configure(path, sso)
    elif menu == "Deploy":
        print(' ')
        print('Deploying...')
        print(' ')
        deploy(path)
    elif menu == "Destroy":
        print(' ')
        print('Destroying...')
        print(' ')
        destroy(path)
    elif menu == "Micropipeline":
        print(' ')
        print('Micropipeline...')
        print(' ')
        micropipeline(path)
    elif menu == "Presets":
        print(' ')
        print('Presets...')
        print(' ')
        presets()
    elif menu == 'Quit':
        print(' ')
        print('Quiting...')
        print(' ')
        quit()

### ALL ACCOUNTS ###

def allaccounts(config, acctlist, value):
    for line in acctlist:
        item = line.split('<->')
        if item[0] != 'All' and item[0] != 'Existing' and item[0] != 'None':
            config[value].append({item[0] : item[1]})
    return config

### ALL REGIONS ###

def allregions(regionlist):
    regionclean = []
    for region in regionlist:
        regionclean.append(region)
    return regionclean

def bootstrap(path):
    print('--------------------------------')
    print('AQUEDUCT BOOTSTRAP')
    print('--------------------------------')
    config = reader(path)

    trusts = ''
    if len(config['cdk_trusts']) != 0:
        for trust in config['cdk_trusts']:
            for key, value in trust.items():
                trusts = trusts+str(value)+','

    lookups = ''
    if len(config['cdk_lookups']) != 0:
        for lookup in config['cdk_lookups']:
            for key, value in lookup.items():
                lookups = lookups+str(value)+','      

    tags = ''
    for tag in config['tags']:
        tags = tags+'--tags '+tag+' '

    for account in config['accounts']:
        for key, value in account.items():
            for region in config['regions']:
                pipeline(config, key, value, region, tags, trusts, lookups)

    print(' ')
    print('Bootstrapping Complete...')
    print(' ')  

    main()

def command(path):
    print('--------------------------------')
    print('AQUEDUCT CLI')
    print('--------------------------------')
    config = reader(path)
    cli = input('cli i.e. aws s3 ls: ').strip()
    print(' ')
    print(cli)
    print(' ')
    print('Correct?')
    print(' ')
    options = [
        "No",
        "Yes"
    ]
    terminal_menu = TerminalMenu(options)
    menu_entry_index = terminal_menu.show()
    
    if options[menu_entry_index] == 'Yes':
        for account in config['accounts']:
            for key, value in account.items():
                for region in config['regions']:
                    print('--------------------------------')
                    print('CLI '+key+' '+str(value)+' '+region)
                    print('--------------------------------')
                    try:
                        os.system(cli+' --profile '+key+' --region '+region)
                        print(' ')
                        print('SUCCESS!!')
                        print(' ')
                    except:
                        print(' ')
                        print('ERROR!!')
                        print(' ')
    print(' ')
    print('Command Completed...')
    print(' ') 
    
    main()
    
def configure(path, sso):
    print('--------------------------------')
    print('AQUEDUCT CONFIGURATION')
    print('--------------------------------')
    config = reader(path)
    sso_start_url = input('SSO Start URL ['+config['sso_start_url']+']: ').strip() or config['sso_start_url']
    sso_region = input('SSO Region ['+config['sso_region']+']: ').strip() or config['sso_region']
    sso_role = input('SSO Role ['+config['sso_role']+']: ').strip() or config['sso_role']
    cli_region = input('CLI Region ['+config['cli_region']+']: ').strip() or config['cli_region']
    cli_output = input('CLI Output ['+config['cli_output']+']: ').strip() or config['cli_output']
    cdk_qualifier = input('CDK Qualifier ['+config['cdk_qualifier']+']: ').strip() or config['cdk_qualifier']
    config['sso_start_url'] = sso_start_url
    config['sso_region'] = sso_region
    config['sso_role'] = sso_role
    config['cli_region'] = cli_region
    config['cli_output'] = cli_output
    config['cdk_qualifier'] = cdk_qualifier

    ### ORAGANIZATION LIST ACCOUNTS ###

    acctlist = []
    acctlist.append('All')
    acctlist.append('Existing')
    acctlist.append('None')
    
    try:
        client = boto3.client('organizations')
        paginator = client.get_paginator('list_accounts')
        response_iterator = paginator.paginate()
        for page in response_iterator:
            for item in page['Accounts']:
                if item['Status'] == 'ACTIVE':
                    acctlist.append(item['Name'].replace(" ","")+'<->'+str(item['Id']))
    except:
        print(' ')
        print('Missing IAM Permission --> organizations:ListAccounts')
        print(' ')
        sys.exit(1)
        pass

    print('--------------------------------')
    print('CDK TRUST ACCOUNT(S)')
    print('--------------------------------')
    
    value = 'cdk_trusts'

    terminal_menu = TerminalMenu(
        acctlist,
        multi_select = True,
        show_multi_select_hint = True
    )
    menu_entry_indices = terminal_menu.show()
    
    if 'All' in terminal_menu.chosen_menu_entries:
        config = allaccounts(config, acctlist, value)
    elif 'Existing' in terminal_menu.chosen_menu_entries:
        config[value] = config[value]
    elif 'None' in terminal_menu.chosen_menu_entries:
        config[value] = []
    else:
        config = allaccounts(config, terminal_menu.chosen_menu_entries, value)
     
    print('--------------------------------')
    print('CDK LOOKUP ACCOUNT(S)')
    print('--------------------------------')

    value = 'cdk_lookups'
    
    terminal_menu = TerminalMenu(
        acctlist,
        multi_select = True,
        show_multi_select_hint = True
    )
    menu_entry_indices = terminal_menu.show()
    
    if 'All' in terminal_menu.chosen_menu_entries:
        config = allaccounts(config, acctlist, value)
    elif 'Existing' in terminal_menu.chosen_menu_entries:
        config[value] = config[value]
    elif 'None' in terminal_menu.chosen_menu_entries:
        config[value] = []
    else:
        config = allaccounts(config, terminal_menu.chosen_menu_entries, value)

    print('--------------------------------')
    print('CDK DEPLOY ACCOUNT(S)')
    print('--------------------------------')

    value = 'accounts'
    
    terminal_menu = TerminalMenu(
        acctlist,
        multi_select = True,
        show_multi_select_hint = True
    )
    menu_entry_indices = terminal_menu.show()
    
    if 'All' in terminal_menu.chosen_menu_entries:
        config = allaccounts(config, acctlist, value)
    elif 'Existing' in terminal_menu.chosen_menu_entries:
        config[value] = config[value]
    elif 'None' in terminal_menu.chosen_menu_entries:
        config[value] = []
    else:
        config = allaccounts(config, terminal_menu.chosen_menu_entries, value)

    ### LIST ACTIVE REGIONS ###

    regionlist = []
    regionlist.append('All')
    regionlist.append('Existing')
    regionlist.append('None')
    
    try:
        client = boto3.client('ec2')
        regions = client.describe_regions()
        for region in regions['Regions']:
            regionlist.append(region['RegionName'])
    except:
        print(' ')
        print('Missing IAM Permission --> ec2:DescribeRegions')
        print(' ')
        sys.exit(1)
        pass

    print('--------------------------------')
    print('CDK DEPLOY REGION(S)')
    print('--------------------------------')

    value = 'regions'

    terminal_menu = TerminalMenu(
        regionlist,
        multi_select = True,
        show_multi_select_hint = True
    )
    menu_entry_indices = terminal_menu.show()
    
    if 'All' in terminal_menu.chosen_menu_entries:
        regionlist.remove('All')
        regionlist.remove('Existing')
        regionlist.remove('None')
        config[value] = regionlist
    elif 'Existing' in terminal_menu.chosen_menu_entries:
        config[value] = config[value]
    elif 'None' in terminal_menu.chosen_menu_entries:
        config[value] = []
    else:
        config[value] = allregions(terminal_menu.chosen_menu_entries)

    print('--------------------------------')
    print('CDK DEPLOY TAG(S)')
    print('--------------------------------')

    print(' ')
    print('Add Tag?')
    print(' ')
    options = [
        "No",
        "Yes"
    ]
    terminal_menu = TerminalMenu(options)
    menu_entry_index = terminal_menu.show()
    
    if options[menu_entry_index] == 'Yes':
        config['tags'] = tagger(config['tags'])

    ### SAVE CONFIGURATION ###

    writer(path, config)
    
    ### SSO SETUP ###
    
    config = reader(path)
    
    cfgfile = open(sso,'w')
    for account in config['accounts']:
        for key, value in account.items():
            cfgfile.write('[profile '+key+']\n')
            cfgfile.write('credential_process = aws-sso-util credential-process --profile '+key+'\n')
            cfgfile.write('sso_start_url = '+config['sso_start_url']+'\n')    
            cfgfile.write('sso_region = '+config['sso_region']+'\n')
            cfgfile.write('sso_account_id = '+str(value)+'\n')
            cfgfile.write('sso_role_name = '+config['sso_role']+'\n')
            cfgfile.write('region = '+config['cli_region']+'\n')
            cfgfile.write('output = '+config['cli_output']+'\n\n')
    cfgfile.close()
    
    print(' ')
    print('SSO Setup Complete...')
    print(' ')    
    
    main()

def deploy(path):
    print('--------------------------------')
    print('AQUEDUCT DEPLOY DIRECTORY')
    print('--------------------------------')
    config = reader(path)
    
    dirs = []
    dirs.append('None')
    directorys = os.listdir('.')
    for directory in directorys:
        checkdir = os.path.isdir(directory)
        if checkdir == True:
            dirs.append(directory)
    
    terminal_menu = TerminalMenu(dirs)
    menu_entry_index = terminal_menu.show()
    
    if dirs[menu_entry_index] != 'None':
        package = dirs[menu_entry_index]
        checkvenv = os.path.isdir(os.path.join(package, '.venv'))
        if checkvenv == False:
            os.system('cd '+package+' && python3 -m venv .venv')
        os.system('cd '+package+' && source .venv/bin/activate && pip3 install -r requirements.txt --upgrade')
        for account in config['accounts']:
            for key, value in account.items():
                print('--------------------------------')
                print('Deploy '+key+' '+str(value))
                print('--------------------------------')
                os.system('cd '+package+' && source .venv/bin/activate && cdk deploy --profile '+key+' --all --require-approval never')

    print(' ')
    print('Deployment Completed...')
    print(' ')    
    
    main()

def destroy(path):
    print('--------------------------------')
    print('AQUEDUCT DESTROY DIRECTORY')
    print('--------------------------------')
    config = reader(path)
    
    dirs = []
    dirs.append('None')
    directorys = os.listdir('.')
    for directory in directorys:
        checkdir = os.path.isdir(directory)
        if checkdir == True:
            dirs.append(directory)
    
    terminal_menu = TerminalMenu(dirs)
    menu_entry_index = terminal_menu.show()
    
    if dirs[menu_entry_index] != 'None':
        package = dirs[menu_entry_index]
        checkvenv = os.path.isdir(os.path.join(package, '.venv'))
        if checkvenv == False:
            os.system('cd '+package+' && python3 -m venv .venv')
        os.system('cd '+package+' && source .venv/bin/activate && pip3 install -r requirements.txt --upgrade')
        for account in config['accounts']:
            for key, value in account.items():
                print('--------------------------------')
                print('Destroy '+key+' '+str(value))
                print('--------------------------------')
                os.system('cd '+package+' && source .venv/bin/activate && cdk destroy --profile '+key+' --all --force')

    print(' ')
    print('Destroying Complete...')
    print(' ')    
    
    main()

def micropipeline(path):
    print('--------------------------------')
    print('CONDUIT MICROPIPELINE')
    print('--------------------------------')
    config = reader(path)

    dirs = []
    dirs.append('None')
    directorys = os.listdir('.')
    for directory in directorys:
        checkdir = os.path.isdir(directory)
        if checkdir == True:
            dirs.append(directory)
    
    terminal_menu = TerminalMenu(dirs)
    menu_entry_index = terminal_menu.show()
    package = dirs[menu_entry_index]

    print('PATH: '+package)
    
    if package != 'None':

        trusts = []
        for trust in config['cdk_trusts']:
            for key, value in trust.items():
                trusts.append(key+'<->'+str(value))
        
        terminal_menu = TerminalMenu(trusts)
        menu_entry_index = terminal_menu.show()
        
        account = trusts[menu_entry_index].split('<->')
        
        print('TRUST: '+str(account[1]))
        
        region_name = config['cli_region']
        
        print('CLI REGION: '+region_name)
        
        s3_client = boto3.client('s3')
        lambda_client = boto3.client('lambda')
        conduit_name = 'conduit-micropipeline-'+str(account[1])+'-'+region_name
        
        options = [
            "None",
            "Deploy",
            "Destroy"
        ]
        terminal_menu = TerminalMenu(options)
        menu_entry_index = terminal_menu.show()
    
        if options[menu_entry_index] != 'None':
            
            action = options[menu_entry_index]

            for account in config['accounts']:
                for key, value in account.items():
                    for region in config['regions']:
                        print('--------------------------------')
                        print(action+' '+key+' '+str(value)+' '+region)
                        print('--------------------------------')
                        
                        package_name = key+'-'+package
                        
                        os.system('cp -R '+package+' '+package_name)
            
                        f = open(package_name+'/app.py', 'r')
                        data = f.read()
                        data = data.replace("os.getenv('CDK_DEFAULT_ACCOUNT')", "'"+str(value)+"'")
                        data = data.replace("os.getenv('CDK_DEFAULT_REGION')", "'"+region+"'")
                        f.close()

                        f = open(package_name+'/app.py', 'w')
                        f.write(data)
                        f.close()            
                        
                        os.system('zip -r '+package_name+'.zip '+package_name)
                        
                        s3_client.upload_file(package_name+'.zip', conduit_name, package_name+'.zip')

                        bundle = {}
                        bundle['bundle'] = package_name+'.zip'
                        bundle['type'] = action.lower()

                        lambda_client.invoke(
                            FunctionName = conduit_name,
                            InvocationType = 'Event',
                            Payload = json.dumps(bundle)
                        )
                        
                        time.sleep(1)

                        os.system('rm -rf '+package_name)
                        os.system('rm '+package_name+'.zip')

    print(' ')
    print('Micropipeline Completed...')
    print(' ') 
    
    main()

def pipeline(config, key, value, region, tags, trusts, lookups):
    
    command = 'export CDK_NEW_BOOTSTRAP=1 && cdk bootstrap aws://'+str(value)+'/'+region+ \
    ' --cloudformation-execution-policies arn:aws:iam::aws:policy/AdministratorAccess --profile '+ \
    key+' --toolkit-stack-name cdk-bootstrap-'+config['cdk_qualifier']+'-'+str(value)+'-'+region+ \
    ' --termination-protection --qualifier '+config['cdk_qualifier']
    
    if len(tags) != 0:
        command = command+' '+tags
        
    if len(trusts) != 0:
        command = command+' --trust '+trusts[:-1]
        
    if len(lookups) != 0:
        command = command+' --trust-for-lookup '+lookups[:-1]
    
    os.system(command)

def presets():
    print('--------------------------------')
    print('AQUEDUCT PRESETS')
    print('--------------------------------')
    print(' ')
    print('Directory:')
    print(' ')
    os.system('pwd')
    print(' ')
    
    options = [
        "cdk init app --language python",
        "python3 -m venv .venv",
        "source .venv/bin/activate",
        "pip3 install -r requirements.txt --upgrade",
        "npm install -g aws-cdk",
        "Exit!"
    ]
    terminal_menu = TerminalMenu(options)
    menu_entry_index = terminal_menu.show()
    
    if options[menu_entry_index] != 'Exit!':
        os.system(options[menu_entry_index])
    
    main()
    
def quit():
        
    ### AWS-SSO-UTIL LOGOUT ###
    print(' ')
    print('Log Out?')
    print(' ')
    options = [
        "No",
        "Yes"
    ]
    terminal_menu = TerminalMenu(options)
    menu_entry_index = terminal_menu.show()
    
    if options[menu_entry_index] == 'No':
        print(' ')
        print('Exited!')
        print(' ')
    else:
        os.system('aws-sso-util logout')
        print(' ')
        print('Logged Out!')
        print(' ')
    sys.exit(1)

def reader(path):
    with open(path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    f.close()
    return config

def tagger(tags):
    status = 'Start'
    
    tag = input('tag i.e. key=value: ').strip()
    tags.append(tag)

    while status != 'Done':
        
        options = [
            "Add",
            "Clear",
            "Done"
        ]
        terminal_menu = TerminalMenu(options)
        menu_entry_index = terminal_menu.show()
        
        if options[menu_entry_index] == 'Add':
            tag = input('tag i.e. key=value: ').strip()
            tags.append(tag)
        elif options[menu_entry_index] == 'Clear':
            tags = []
        elif options[menu_entry_index] == 'Done':
            status = 'Done'
    
    return tags

def writer(path, config):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=4)
    f.close()
    print(' ')
    print('Saved!')
    print(' ')

def main():

    ### AWSCLIv2 CHECK ###
    p = run( [ 'aws', '--version' ], capture_output=True )
    #print( 'exit status:', p.returncode )
    #print( 'stdout:', p.stdout.decode() )
    #print( 'stderr:', p.stderr.decode() )
    try:
        awscliversion = p.stderr.decode()[8]
    except:
        awscliversion = p.stdout.decode()[8]
        pass
    
    if awscliversion != '2':
        print('--------------------------------')
        print('AWSCLIv2 - PRE-REQUISITE')
        print('--------------------------------')
        print('$ curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"')
        print('$ unzip awscliv2.zip')
        print('$ sudo ./aws/install')
        print('$ aws --version')
        print(' ')
        print('https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html')
        print(' ')
        sys.exit(1)

    ### AWS-SSO-UTIL CHECK ###
    try:
        p = run( [ 'aws-sso-util', '--help' ], capture_output=True )
        awsssoutil = 'YES'
        #print( 'exit status:', p.returncode )
        #print( 'stdout:', p.stdout.decode() )
        #print( 'stderr:', p.stderr.decode() )
    except:
        awsssoutil = 'NO'
        pass
    
    if awsssoutil == 'NO':
        print('--------------------------------')
        print('AWS-SSO-UTIL - PRE-REQUISITE')
        print('--------------------------------')
        print('$ pip install aws-sso-util')
        print(' ')
        print('https://github.com/benkehoe/aws-sso-util')
        print(' ')
        sys.exit(1)

    ### AQUEDUCT CONFIGURATION ###

    awsdir = '.aws'
    configfile = 'aqueduct'
    ssofile = 'config'
    homedir = os.path.expanduser('~')
    checkdir = os.path.isdir(os.path.join(homedir, awsdir))
    pathconfig = os.path.join(homedir, awsdir, configfile)
    ssoconfig = os.path.join(homedir, awsdir, ssofile)

    ### CHECK DIRECTORY EXISTS ###

    if checkdir == False:
        os.makedirs(os.path.join(homedir, awsdir))
    
    ### CHECK CONFIG EXISTS ###

    checkconfig = os.path.isfile(os.path.join(homedir, awsdir, configfile))
    
    if checkconfig == False:
        print('--------------------------------')
        print('AQUEDUCT INITIAL SETUP')
        print('--------------------------------')
        sso_start_url = input('SSO Start URL [ ]: ').strip()
        sso_region = input('SSO Region [ ]: ').strip()
        sso_role = input('SSO Role [AWSAdministratorAccess]: ').strip() or 'AWSAdministratorAccess'
        cli_region = input('CLI Region [ ]: ').strip()
        cli_output = input('CLI Output [json]: ').strip() or 'json'
        cdk_qualifier = input('CDK Qualifier [ ]: ').strip()
        cdk_trusts = []
        cdk_lookups = []
        accounts = []
        regions = []
        tags = []
    
        config = {}
        config['sso_start_url'] = sso_start_url
        config['sso_region'] = sso_region
        config['sso_role'] = sso_role
        config['cli_region'] = cli_region
        config['cli_output'] = cli_output
        config['cdk_qualifier'] = cdk_qualifier
        config['cdk_trusts'] = cdk_trusts
        config['cdk_lookups'] = cdk_lookups
        config['accounts'] = accounts
        config['regions'] = regions
        config['tags'] = tags
    
        with open(os.path.join(homedir, awsdir, configfile), 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=4)
        f.close()

    ### AWS-SSO-UTIL LOGIN ###
    
    config = reader(pathconfig)

    os.system('export AWS_DEFAULT_SSO_START_URL='+config['sso_start_url']+ \
              '&& export AWS_DEFAULT_SSO_REGION='+config['sso_region']+ \
              '&& aws-sso-util login')

    ### AQUEDUCT MENU ###
    
    print('--------------------------------')
    print('AQUEDUCT v'+__version__)
    print('--------------------------------')
    
    options = [
        "Bootstrap",
        "Command",
        "Configure",
        "Deploy",
        "Destroy",
        "Micropipeline",
        "Presets",
        "Quit"
    ]
    terminal_menu = TerminalMenu(options)
    menu_entry_index = terminal_menu.show()
    action(options[menu_entry_index], pathconfig, ssoconfig)
