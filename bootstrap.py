import os
from subprocess import call
from tempfile import TemporaryFile
import sys
import shutil

REQUIREMENTS = ['virtualenv', 'hg', 'git']

def check_requirements():
    "Check requirements"
    output = TemporaryFile(mode='rwt')
    pos = 0
    for req in REQUIREMENTS:
        if 0 != call(['which', req], stdout=output, stderr=output):
            # get call output
            output.seek(pos)
            err = output.read()
            print "ERROR: %s is not satisfied (%s)" % (req, err)
            sys.exit(1)
        pos = output.tell()


def provide_local_settings():
    "Check if local_settings.py exists"
    if not os.path.exists('local_settings.py'):
        shutil.copyfile('local_settings.py.def', 'local_settings.py')
        print "Local settings did not exist, default local settings has been provided."
        print "Please, check local_settings.py and modify it if needed."


def provide_virtualenv():
    "Check if virtualenv exists"
    if not os.path.exists('ve'):
        call(["virtualenv", "--distribute", "ve"])


def install_pip_requirements():
    "Install python requirements into virtual environment"
    call(['ve/bin/pip', 'install', '-r', 'requirements.txt'])


def do(func, *args, **kwargs):
    "Announce func.__doc__ and run func with provided arguments"
    doc = getattr(func, '__doc__')
    if doc is None:
        # compose it
        func_args = ','.join([repr(a) for a in args])
        func_kwargs = ','.join("%s=%s" % (k, repr(v)) for k,v in kwargs.iteritems())
        doc = "%s(%s)" % (func.__name__, ','.join([func_args, func_kwargs]))
    print doc
    return func(*args, **kwargs)


def bootstrap_main():
    do(check_requirements)
    do(provide_local_settings)
    do(provide_virtualenv)
    do(install_pip_requirements)
    print "Done"

if __name__ == '__main__':
    do(bootstrap_main)
