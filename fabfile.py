# -*- coding: utf-8 -*-
from fabric.api import run
from fabric.api import cd
from fabric.api import env
from fabric.api import execute
import getpass
from fabric.api import settings
from fabric.api import hosts
from fabric.api import sudo
from fabric.api import roles
from fabric.api import prefix
from fabric.api import local
from fabric.contrib import django
import sys
import os
PROJECT_NAME = 'smirik'
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

env.use_ssh_config = True
env.hosts = ['onetap@one-tap.ru']
env.path = BASE_DIR+".venv/bin/activate"

root_dir = '/www/smirik/'
PRODUCTION = {
        'root_dir': root_dir,
        'env_script': '%s/.venv/bin/activate' % root_dir,
        'libs': '%s/.venv/lib/python2.7/site-packages/' % root_dir,
}

activate = env.path


def restart():
    """Method for restarting process of web-service"""
    run("kill `cat %s/.pid`" % root_dir)
    #run("kill -9 `cat %s/.celery_pid`" % root_dir)

def update():
    """Method for updating code"""

    # Update code.
    local("git push origin master")
    with cd(PRODUCTION['root_dir']):
        run("git pull origin master")

    #Update markup.
    proj_dir = os.path.abspath(__file__)
    with cd(os.path.join(proj_dir, PROJECT_NAME, 'static', 'markup')):
        local("git push origin master")

    with cd(os.path.join(PRODUCTION['root_dir'], PROJECT_NAME, 'static', 'markup')):
        run("git pull origin master")


def backup():
    with cd(PRODUCTION['root_dir']):
        command = "`DJANGO_SETTINGS_MODULE=%s.settings python2.7 -c" % PROJECT_NAME
        addition_path = "import sys; sys.path.insert(0, '%s');" % PRODUCTION['root_dir']
        addition_path += " import site; site.addsitedir('%s')" % PRODUCTION['libs']
        base_str = "%s \"%s; from django.conf import settings as sts; print sts.DATABASES['default']" % (command,
                addition_path)
        user = "%s['USER']\"`" % base_str
        name = "%s['NAME']\"`" % base_str
        host = "%s['HOST']\"`" % base_str
        port = "%s['PORT']\"`" % base_str
        cmd = "pg_dump --host=%s --port=%s --username=%s -d %s > dump.sql" % (host,
            port, user, name)
        run("source %s" % PRODUCTION['env_script'])
        run(cmd)


def migrate():
    backup()    # Make backup for any case.
    with cd(PRODUCTION['root_dir']):
        with prefix("source %s" % PRODUCTION['env_script']):
            run("./manage.py migrate")


def install_deps():
    with cd(PRODUCTION['root_dir']):
        with prefix("source %s" % PRODUCTION['env_script']):
            run("pip install -r reqs.pip")



def collect():
    with cd(PRODUCTION['root_dir']):
        with prefix("source %s" % PRODUCTION['env_script']):
            run("./manage.py collectstatic --noinput")



def deploy():
    update()
    backup()
    install_deps()
    collect()
    migrate()
    restart()
