import pathlib
import typer
import aqueduct.deployment as _deploy
import aqueduct.destruction as _destroy
import aqueduct.identity as _idp

app = typer.Typer()

@app.command()
def deploy():
    _deploy.deploy()

@app.command()
def destroy():
    _destroy.destroy()

@app.command()
def hints():
    print('npm install -g aws-cdk')
    print('npm install -g npm@9.6.7')
    print('npm install -g node@18.0.0 --force')
    print('cdk init app --language python')
    print('python3 -m venv .venv')
    print('source .venv/bin/activate')
    print('pip3 install -r requirements.txt --upgrade')
    print('echo .~c9* > ~/.gitignore')
    print('echo cdk.context.json >> ~/.gitignore')
    print('git config --global core.excludesfile ~/.gitignore')

@app.command()
def login():
    _idp.login()

@app.command()
def logout():
    _idp.logout()

@app.command()
def nag():
    rules = []
    output = pathlib.Path.joinpath(pathlib.Path().absolute(),'cdk.out')
    for p in pathlib.Path(output).glob('*'):
        if p.name.startswith('AwsSolutions') or p.name.startswith('HIPAA.Security') \
          or p.name.startswith('NIST.800.53.R5') or p.name.startswith('PCI.DSS.321'):
            read = pathlib.Path.joinpath(output,p.name)
            with open(read) as f:
                f.readline()
                for line in f:
                    parse = line.split('"')
                    if parse[1] not in rules:
                        rules.append(parse[1])
                        print('\t\t{"id":"'+parse[1]+'","reason":"'+parse[11]+'"},')      

if __name__ == "__main__":
    app()
