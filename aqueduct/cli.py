import argparse
import json
import os
from aqueduct import __version__

def addacct(pathconfig):
    config = configread(pathconfig)
    account_name = input('Account Name [ ]: ').strip()
    account_number = input('Account Number [ ]: ').strip()
    config['accounts'].append({account_name : account_number})
    configwrite(pathconfig,config)

def addreg(pathconfig):
    config = configread(pathconfig)
    region = input('Region [ ]: ').strip()
    config['regions'].append(region)
    configwrite(pathconfig,config)

def addtag(pathconfig):
    config = configread(pathconfig)
    tag = input('tag i.e. key=value: ').strip()
    config['tags'].append(tag)
    configwrite(pathconfig,config)

def bootstrap(pathconfig):
    config = configread(pathconfig)
    tags = taglist(config)
    for account in config['accounts']:
        for key, value in account.items():
            for region in config['regions']:
                pipeline(config, key, value, region, tags)

def configread(pathconfig):
    with open(pathconfig, 'r', encoding='utf-8') as f:
        config = json.load(f)
    f.close()
    return config

def configwrite(pathconfig,config):
    with open(pathconfig, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=4)
    f.close()

def delacct(pathconfig):
    config = configread(pathconfig)
    account_name = input('Account Name [ ]: ').strip()
    account_number = input('Account Number [ ]: ').strip()
    for i in range(len(config['accounts'])):
        if config['accounts'][i].get(account_name) == account_number:
            del config['accounts'][i]
    configwrite(pathconfig,config)

def delreg(pathconfig):
    config = configread(pathconfig)
    region = input('Region [ ]: ').strip()
    config['regions'].remove(region)
    configwrite(pathconfig,config)

def deltag(pathconfig):
    config = configread(pathconfig)
    tag = input('tag i.e. key=value: ').strip()
    config['tags'].remove(tag)
    configwrite(pathconfig,config)

def deployall(pathconfig):
    config = configread(pathconfig)
    package = input('CDK Package [ ]: ').strip()
    checkpkg = os.path.isdir(package)
    if checkpkg == False:
        print('CDK Package Unavailable')
    else:
        checkvenv = os.path.isdir(os.path.join(package, '.venv'))
        if checkvenv == False:
            os.system('cd '+package+' && python3 -m venv .venv')
        os.system('cd '+package+' && source .venv/bin/activate && pip3 install -r requirements.txt --upgrade')
    for account in config['accounts']:
        for key, value in account.items():
            os.system('cd '+package+' && source .venv/bin/activate && cdk deploy --profile '+ \
            key+' --all --require-approval never')

def destroyall(pathconfig):
    config = configread(pathconfig)
    package = input('CDK Package [ ]: ').strip()
    checkpkg = os.path.isdir(package)
    if checkpkg == False:
        print('CDK Package Unavailable')
    else:
        checkvenv = os.path.isdir(os.path.join(package, '.venv'))
        if checkvenv == False:
            os.system('cd '+package+' && python3 -m venv .venv')
        os.system('cd '+package+' && source .venv/bin/activate && pip3 install -r requirements.txt --upgrade')
    for account in config['accounts']:
        for key, value in account.items():
            os.system('cd '+package+' && source .venv/bin/activate && cdk destroy --profile '+ \
            key+' --all --force')

def pipeline(config, key, value, region, tags):
    os.system('export CDK_NEW_BOOTSTRAP=1 && cdk bootstrap aws://'+str(value)+'/'+region+ \
    ' --cloudformation-execution-policies arn:aws:iam::aws:policy/AdministratorAccess --trust '+ \
    str(config['cdk_trust'])+' --profile '+key+' --toolkit-stack-name cdk-bootstrap-'+config['cdk_qualifier']+ \
    '-'+str(value)+'-'+region+' --termination-protection --qualifier '+config['cdk_qualifier']+' '+tags)

def ssosetup(pathconfig,ssoconfig):
    config = configread(pathconfig)
    cfgfile = open(ssoconfig,'w')
    for account in config['accounts']:
        for key, value in account.items():
            cfgfile.write('[profile '+key+']\n')
            cfgfile.write('sso_start_url = '+config['sso_start_url']+'\n')    
            cfgfile.write('sso_region = '+config['sso_region']+'\n')
            cfgfile.write('sso_account_id = '+str(value)+'\n')
            cfgfile.write('sso_role_name = '+config['sso_role']+'\n')
            cfgfile.write('region = '+config['cli_region']+'\n')
            cfgfile.write('output = '+config['cli_output']+'\n')
    cfgfile.close()

def taglist(config):
    tags = ''
    for tag in config['tags']:
        tags = tags+'--tags '+tag+' '
    return tags

def main():

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
        sso_start_url = input('SSO Start URL [ ]: ').strip()
        sso_region = input('SSO Region [ ]: ').strip()
        sso_role = input('SSO Role [AWSAdministratorAccess]: ').strip() or 'AWSAdministratorAccess'
        cli_region = input('CLI Region [ ]: ').strip()
        cli_output = input('CLI Output [json]: ').strip() or 'json'
        cdk_qualifier = input('CDK Qualifier [ ]: ').strip()
        cdk_trust = input('CDK Trust [ ]: ').strip()
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
        config['cdk_trust'] = cdk_trust
        config['accounts'] = accounts
        config['regions'] = regions
        config['tags'] = tags
    
        with open(os.path.join(homedir, awsdir, configfile), 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=4)
        f.close()
        
    ### AQUEDUCT OPTIONS ###

    parser = argparse.ArgumentParser(description = 'aqueduct v'+__version__)
    parser.add_argument('--addacct', action='store_true', help='Add Account')
    parser.add_argument('--addreg', action='store_true', help='Add Region')
    parser.add_argument('--addtag', action='store_true', help='Add Tag')
    parser.add_argument('--bootstrap', action='store_true', help='Bootstrap CDK')
    parser.add_argument('--delacct', action='store_true', help='Delete Account')
    parser.add_argument('--delreg', action='store_true', help='Delete Region')
    parser.add_argument('--deltag', action='store_true', help='Delete Tag')
    parser.add_argument('--deployall', action='store_true', help='Deploy All')
    parser.add_argument('--destroyall', action='store_true', help='Destroy All')
    parser.add_argument('--ssosetup', action='store_true', help='SSO Setup')
    args = parser.parse_args()

    if(args.addacct):
        addacct(pathconfig)
    elif(args.addreg):
        addreg(pathconfig)
    elif(args.addtag):
        addtag(pathconfig)
    elif(args.bootstrap):
        bootstrap(pathconfig)    
    elif(args.delacct):
        delacct(pathconfig)
    elif(args.delreg):
        delreg(pathconfig)
    elif(args.deltag):
        deltag(pathconfig)
    elif(args.deployall):
        deployall(pathconfig)
    elif(args.destroyall):
        destroyall(pathconfig)
    elif(args.ssosetup):
        ssosetup(pathconfig,ssoconfig)        
    else:
        print('add -h or --help for usage help')
