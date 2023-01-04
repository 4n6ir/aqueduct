import typer
import aqueduct.deployment as _deploy
import aqueduct.destruction as _destroy
import aqueduct.identity as _idp
import aqueduct.nanopipeline as _nanopipeline

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
    print('cdk init app --language python')
    print('python3 -m venv .venv')
    print('source .venv/bin/activate')
    print('pip3 install -r requirements.txt --upgrade')
    print('echo .~c9* > ~/.gitignore')
    print('git config --global core.excludesfile ~/.gitignore')
    print('git checkout -b dev')

@app.command()
def login():
    _idp.login()

@app.command()
def logout():
    _idp.logout()

app.add_typer(_nanopipeline.app, name='nanopipeline')

if __name__ == "__main__":
    app()
