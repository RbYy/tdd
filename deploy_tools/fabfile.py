
from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run, sudo, prompt
import random
from getpass import getpass


REPO_URL = 'https://github.com/rbyy/tdd.git'

PG_DB_SETTINGS = """
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '%s',
        'USER': '%s',
        'PASSWORD': '%s',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
"""


def deploy(site=None):
    if not site:
        site = env.host
    site_folder = '/home/%s/sites/%s' % (env.user, site)
    source_folder = site_folder + '/source'
    _create_directory_structure_if_necessary(site_folder)
    PG_DB_SETTINGS = _create_pg_database()
    _get_latest_source(source_folder)
    _update_settings(source_folder, env.host, PG_DB_SETTINGS)
    _update_virtualenv(source_folder)
    _update_static_files(source_folder)
    _update_database(source_folder)


def _create_directory_structure_if_necessary(site_folder):
    for subfolder in ('database', 'static', 'virtualenv', 'source'):
        run('mkdir -p %s/%s' % (site_folder, subfolder))


def _get_latest_source(source_folder):
    if exists(source_folder + '/.git'):
        run('cd %s && git fetch' % (source_folder,))
    else:
        run('git clone %s %s' % (REPO_URL, source_folder))
    current_commit = local("git log -n 1 --format=%H", capture=True)
    run('cd %s && git reset --hard %s' % (source_folder, current_commit))


def _update_settings(source_folder, site_name):
    settings_path = source_folder + '/gettingstarted/settings.py'
    requirements_path = source_folder + '/requirements.txt'
    sed(settings_path, "DEBUG = True", "DEBUG = False")
    sed(settings_path,
        'ALLOWED_HOSTS =.+$',
        'ALLOWED_HOSTS = ["%s"]' % (site_name,)
        )
    secret_key_file = source_folder + '/gettingstarted/secret_key.py'
    if not exists(secret_key_file):
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        append(secret_key_file, "SECRET_KEY = '%s'" % (key,))
    append(settings_path, '\nfrom .secret_key import SECRET_KEY')
    append(settings_path, '\n%s' % (PG_DB_SETTINGS))
    append(requirements_path, 'psycopg2==2.6.1')


def _update_virtualenv(source_folder):
    virtualenv_folder = source_folder + '/../virtualenv'
    if not exists(virtualenv_folder + '/bin/pip'):
        run('virtualenv --python=python3 %s' % (virtualenv_folder,))
    run('%s/bin/pip install -r %s/requirements.txt' % (
            virtualenv_folder, source_folder
    ))


def _update_static_files(source_folder):
    run('cd %s && ../virtualenv/bin/python3 manage.py collectstatic --noinput' % (
        source_folder,
    ))


def _update_database(source_folder):
    run('cd %s && ../virtualenv/bin/python3 manage.py migrate --noinput' % (
        source_folder,
    ))


def _create_pg_database():
    """Creates role and database"""
    db_user = get_user()
    db_pass = get_pass()
    db_db = get_db()
    pg_db_set = PG_DB_SETTINGS % (db_db, db_user, db_pass)
    sudo('psql -c "CREATE USER %s WITH PASSWORD E\'%s\'"' % (db_user, db_pass), user='postgres')
    sudo('psql -c "CREATE DATABASE %s WITH OWNER %s"' % (db_db, db_user), user='postgres')
    sudo('psql -c "ALTER ROLE %s WITH CREATEDB"' % (db_user), user='postgres')
    return pg_db_set


def get_user():
    return prompt('choose postgres user:')


def get_pass():
    pass_1st = getpass('choose postgres password: ')
    pass_2nd = getpass('repeat postgres password: ')
    if pass_1st == pass_2nd:
        return pass_2nd
    else:

        get_pass()


def get_db():
    return prompt("pg database name: ")
