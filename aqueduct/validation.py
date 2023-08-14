import aws_sso_lib
import pathlib
import typer

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
