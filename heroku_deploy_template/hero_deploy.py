#!/Library/Frameworks/Python.framework/Versions/3.7/bin/python3

'''Auto-deploy a python application to the Heroku Cloud Platform.

Place your application files and dependencies into this directory and run
this script from the command line. This script automatically initializes
the directory, generates all of the necessary auxillary files, and after
entering your login credentials, it deploys your application to Heroku,
configures the dynos and launches the app.

    USAGE:
        python3 hero_deploy.py  dep_type  app_name  app_type  main_exe

        LITERAL SYNTAX:
            python3 hero_deploy.py  create  myApp  worker  myscript  -startapp
            python3 hero_deploy.py  update  -startapp

        MANDATORY ARGUMENTS:
            dep_type: Deployment Type. Either 'create' or 'update'. Use
                     'create' the first time an app is deployed to the
                      cloud and 'update' when making revisions thereafter.

            app_name: Your Application's Name - Must be lowercase and only
                      contain alphanumeric symbols and/or underscores and
                      dashes.

            app_type: Determines Worker Status. Options are either: "web"
                     'or "worker".

            main_exe: Name of Your App's Main Executable File without
                      the extension.

        OPTIONAL ARGUMENTS:
            -startapp: After successful deployment, configure the dynos,
                       run the application and begin logging in the CLI.

    EXTERNAL DEPENDENCIES:
           This script requires the pipreqs module.

           Installation Options:
               From PyPI: pip install pipreqs
               From Github: https://github.com/bndr/pipreqs.git

      write the readme.md
      create the directory
'''
import os
import json
import argparse
import subprocess
from sys import version

HERE = os.getcwd()

with open('parameters.json', 'r') as args:
    PARAMETERS = json.load(args)
    CMDS = PARAMETERS['Cmds']
    ARGS = PARAMETERS['Args']


def parse_args():
    '''Argument Wrangler.
    '''
    arg_parser = argparse.ArgumentParser(description='heroku_deploy')
    subparser = arg_parser.add_subparsers()

    parser_create = subparser.add_parser('create')
    parser_update = subparser.add_parser('update')

    for key, value in ARGS.items():
        if key == 'launch':
            parser_create.add_argument(value[0], action='store_true', help=value[1])
            parser_update.add_argument(value[0], action='store_true', help=value[1])
        elif key == 'update':
            parser_update.add_argument(value[0], action='store_true', help=value[1])
        else:
            parser_create.add_argument(value[0], metavar=value[0], help=value[1])
    return vars(arg_parser.parse_args())


def shellex(cmd, directory, capture=False):
    '''SHELL EXECUTE:
           Execute any system shell command as a non-blocking subprocess.

       ARGUMENTS:
           command: str: any shell command
           directory: str: directory where the subprocess will launch

       USAGE:
           execute('ls -a', '/')
           execute('afplay music.mp3', '$HOME)
           execute("open -a 'Sublime Text' my_script.py" 'home/Documents')
    '''
    with subprocess.Popen(cmd.split(' '), cwd=directory, stdout=subprocess.PIPE) as process:
        stdout, _ = process.communicate()
        if not capture:
            print(stdout.decode('utf-8'))
        return stdout.decode('utf-8')


def generate_procfile(target, apptype='worker'):
    '''Generate the Procfile.

       ARGUMENTS:
           apptype: str: app signature. Either: 'worker' or 'web'.
           target: str: the target script or main application.
    '''
    if not os.path.exists('./Procfile'):
        print('\nGenerating Procfile...')
        with open(f'{HERE}/Procfile', 'w') as file:
            file.write(f'{apptype}: python {target}')

        shellex(f'chmod 744 {HERE}/Procfile', HERE)


def generate_runtime():
    '''Generates the runtime.txt which designates the local version of Python
       to use at runtime on the cloud.
    '''
    print('Creating runtime.txt...')
    with open('./runtime.txt', 'w') as run:
        run.write('python-' + version[:5])


def generate_requirements(update=False):
    '''Generates the requirements.txt using 'pipreqs'
    '''
    cmd = 'pipreqs --force' if update is True else 'pipreqs'
    print('Generating requirements.txt...')
    shellex(f'{cmd} {HERE}', HERE)


def create_app(main_exe, designation):
    '''Initializes local repository; creates auxillary files; deploys app.
    '''
    generate_procfile(main_exe, apptype=designation)
    generate_runtime()
    generate_requirements()

    for index, cmd in enumerate(CMDS[:-2]):
        if index != 5:
            shellex(cmd, HERE)


def update_app():
    '''Updates an app already deployed on the server.
    '''
    generate_requirements(update=True)
    for index, cmd in enumerate(CMDS[3:-2]):
        if index != 1:
            shellex(cmd, HERE)


def start_dynos():
    '''Designate dynos; launch the application; start logging.
    '''
    shellex(CMDS[7], HERE)
    os.system(CMDS[8])


def main():
    arguments = parse_args()
    update = arguments.get('update', False)

    if not update:
        app_name = arguments['app_name']
        app_type = arguments['app_type']
        filename = arguments['filename'] + '.py'

        CMDS[2] = CMDS[2].format(app_name)
        create_app(filename, app_type)
    else:
        update_app()

    if arguments['startapp']:
        start_dynos()


if __name__ == '__main__':
    main()
