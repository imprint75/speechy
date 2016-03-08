from fabric.api import env, run
from fabric.context_managers import cd
from fabric.operations import sudo
from fabric.contrib.files import exists


def vagrant():
    env.hosts = ['192.168.33.103']
    env.user = 'vagrant'
    env.password = 'vagrant'


def testing():
    run('ls')


def build3():
    apt_update()
    add_apt_repo()
    apt_update()
    install_nginx()
    install_uwsgi()
    install_python()
    install_git()
    link_confs('', '')
    create_env('')
    restart()


def make_directory(dir_name='test'):
    with cd('/srv/'):
        if not exists(dir_name):
            sudo('mkdir {}'.format(dir_name))
            sudo('chown {}:{} {}'.format(env.user, dir_name))


def create_env(venv='test'):
    run('cd /home/{}'.format(env.user))
    run('python3 -m venv {}'.format(venv))


def upgrade_distribute(venv='test'):
    #sudo('easy_install -U distribute')
    command = '/home/{}/{}/bin/pip install --upgrade distribute'
    run(command.format(env.user, venv))


def link_confs(dir_name='test', file_name='test'):
    n1 = 'ln -s /srv/{0}/{0}/confs/{1} /etc/nginx/sites-available/{1}'
    sudo(n1.format(dir_name, file_name))
    u1 = 'ln -s /srv/{0}/{0}/confs/{1}.ini /etc/uwsgi/apps-available/{1}.ini'
    sudo(u1.format(dir_name, file_name))
    n2 = 'ln -s /etc/nginx/sites-available/{0} /etc/nginx/sites-enabled/{0}'
    sudo(n2.format(file_name))
    u2 = 'ln -s /etc/uwsgi/apps-available/{0}.ini ' \
         '/etc/uwsgi/apps-enabled/{0}.ini'
    sudo(u2.format(file_name))


def restart():
    sudo('service nginx restart')
    sudo('service uwsgi restart')


### apt-get stuff ###


def add_apt_repo():
    sudo('apt-get install python3-software-properties')


def apt_update():
    sudo('apt-get update')


### ssh key stuff ###


### installs ###


def install_nginx():
    sudo('apt-get install nginx-full')


def install_uwsgi():
    sudo('apt-get install uwsgi uwsgi-plugin-python3')


def install_python():
    sudo('apt-get install python3-setuptools')
    sudo('apt-get install python3.4-venv')
    sudo('apt-get install python3-dev')
    sudo('apt-get install build-essential')


def install_git():
    run('sudo apt-get install git')


def install_emacs24():
    apt_update()
    sudo('apt-get install emacs24 emacs24-el emacs24-common-non-dfsg')


def install_twisted():
    #sudo('add-apt-repository ppa:twisted-dev/ppa')
    #apt_update()
    sudo('apt-get install python-twisted')


def install_node():
    sudo('add-apt-repository ppa:chris-lea/node.js')
    sudo('apt-get update')
    sudo('apt-get install python g++ make nodejs')


def install_mysql():
    sudo('apt-get install mysql-server mysql-client')
    sudo('apt-get install libmysqlclient-dev')


def create_mysql_db(password=None):
    user = 'root'
    dbname = 'test'
    if password:
        run('mysqladmin -u {} -p{} create {}'.format(user, password, dbname))
    else:
        run('mysqladmin -u {} create {}'.format(user, dbname))


def apt_get(*packages):
    sudo('apt-get -y --no-upgrade install %s' % ' '.join(packages),
         shell=False)
