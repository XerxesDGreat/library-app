__author__ = 'josh'

import git_updater
from git_updater.models import Version
import pycurl
from StringIO import StringIO
import json
from library_app import settings
import os
import sys
import shutil
import tarfile
import time
import math
from django.core.management import call_command
import datetime
import pytz
from django.template import loader
from django.template.context import Context
import subprocess

from django.core.urlresolvers import reverse

from django.core.cache import cache

CACHE_TTL = 4 * 60 * 60
CACHE_KEY = 'git_recent_versions'
CURL_CONNECT_TIMEOUT = 3
CURL_OP_TIMEOUT = 3

def get_current_version():
    return git_updater.__version__

def get_available_updates():
    '''
    Fetches all versions later than the current version
    :return:
    '''
    my_version = Version.from_string(get_current_version())
    git_versions = get_recent_versions()
    num_newer = 0
    for v in git_versions:
        this_version = Version.from_string(v.get('tag_name'))
        if this_version == my_version:
            break
        num_newer += 1
    return git_versions[0:num_newer]

def get_recent_versions(num_versions=10):
    '''
    Gets the recent versions from github
    :param num_versions:
    :return:
    '''
    response = cache.get(CACHE_KEY)
    if not response:
        c = pycurl.Curl()
        rbuf = StringIO()
        c.setopt(c.URL, 'https://api.github.com/repos/XerxesDGreat/library-app/releases?per_page=%d' % num_versions)
        c.setopt(c.WRITEDATA, rbuf)
        c.setopt(pycurl.CONNECTTIMEOUT, CURL_CONNECT_TIMEOUT)
        c.setopt(pycurl.TIMEOUT, CURL_OP_TIMEOUT)
        c.perform()
        response = rbuf.getvalue()
        c.close()
        response = json.loads(response)
        response = [_clean_change(x) for x in response]
        cache.set(CACHE_KEY, response, CACHE_TTL)

    return response

def _clean_change(change):
    change['body'] = [x.lstrip('- ') for x in change['body'].split('\r\n')]
    d_string = change['created_at'].replace('Z', '')
    dt = datetime.datetime.strptime(d_string, '%Y-%m-%dT%H:%M:%S')
    pac = pytz.timezone('America/Los_Angeles')
    change['created_at'] = dt.replace(tzinfo=pytz.utc).astimezone(pac)
    return change

def do_update():
    '''
    Performs the work of updating, controlling the various steps
    :return:
    '''
    t = loader.get_template('updates/update_progress.html')
    c = Context()
    yield t.render(c)

    redir = '<script type="text/javascript">doneWithUpdate();</script>'
    available_updates = get_available_updates()
    if len(available_updates) == 0:
        yield 'nothing to be done' + redir
    else:
        old = sys.stdout
        sys.stdout = StringIO()
        target_version_info = available_updates[0]
        print 'updating to %s' % target_version_info['tag_name']
        yield _flush()

        working_dir = os.path.join(settings.BASE_DIR, '.updater')
        if not os.path.isdir(working_dir):
            os.mkdir(working_dir)
        yield _flush()

        downloaded_file = _download_update(working_dir, target_version_info)
        update_success = False
        if downloaded_file:
            for a in _apply_update(downloaded_file, target_version_info):
                yield a

        applied_updates = []
        if update_success:
            for u in available_updates:
                applied_updates.append({
                    'version': u['tag_name'],
                    'name': u['name'],
                    'description': u['body'],
                    'date': u['published_at']
                })

        sys.stdout = old
        yield redir

def _download_update(dest_dir, update_info):
    '''
    Handles downloading the update file and making it available to be extracted and applied
    :param dest_dir:
    :param update_info:
    :rtype basestring:
    '''
    target_file = os.path.join(dest_dir, update_info['tag_name'] + '.tar.gz')
    if os.path.isfile(target_file):
        print 'File %s already exists; not downloading' % target_file
        return target_file

    print 'Downloading new version and placing into %s' % target_file
    c = pycurl.Curl()
    c.setopt(c.URL, update_info['tarball_url'])
    b = StringIO()
    c.setopt(c.WRITEDATA, b)
    c.setopt(c.FOLLOWLOCATION, True)
    c.perform()
    c.close()
    with open(target_file, 'w') as outfile:
        outfile.write(b.getvalue())

    print 'Download complete'
    return target_file

def _flush():
    a = sys.stdout.getvalue()
    a = a.replace('\n', '<br />') + '<br />'
    sys.stdout.truncate(0)
    return a

def _apply_update(tar_file_path, update_info):
    '''
    Does the work of applying the changes to the files and updating the current version
    :param src_dir:
    :param update_info:
    :return:
    '''

    print 'Starting update!'
    yield _flush()
    print 'backing up database (this is a <em>LOOOOONG</em> step!)'
    yield(_flush())
    #_backup_db()
    yield _flush()

    print 'Extracting update files'
    yield _flush()
    _extract_update(tar_file_path)
    yield _flush()

    update_dir = settings.BASE_DIR
    extracted_dir = _get_extracted_dir(os.path.dirname(tar_file_path))
    print 'copying files from %s to %s' % (extracted_dir, update_dir)
    yield _flush()

    #_copy(extracted_dir, update_dir)
    yield _flush()

    print 'Installing new packages'
    yield _flush()
    _pip_install()
    yield _flush()

    print 'Migrating database'
    yield _flush()
    _migrate_db()
    yield _flush()

    cache.delete(CACHE_KEY)

    print "Update completed! You'll be redirected in a few seconds; if you don't want to wait, <a href='%s'>click here</a>" % reverse('git_updater:update_list')
    yield _flush()

def _pip_install():
    ve_dir = os.path.dirname(sys.executable)
    command = '%s/pip' % ve_dir

    output = subprocess.check_output(['%s/pip' % ve_dir, 'install', '-r', 'requirements.txt'], stderr=subprocess.STDOUT)

    print output
    print 'packages updated'


def _backup_db():
    backup_dir = os.path.join(settings.BASE_DIR, 'backup')
    if not os.path.isdir(backup_dir):
        os.mkdir(backup_dir)

    fname = 'db_backup_%d.json' % math.floor(time.time())
    backup_target = os.path.join(backup_dir, fname)

    with open(backup_target, 'w') as f:
        call_command('dumpdata', stdout=f)

    print 'database backed up to %s' % backup_target

def _extract_update(tar_file_path):
    if not tarfile.is_tarfile(tar_file_path):
        print '%s is not a valid tarfile; try rerunning' % tar_file_path
        return False

    extract_container_dir = os.path.dirname(tar_file_path)
    if not os.path.isdir(extract_container_dir):
        return False

    print 'extracting to %s' % tar_file_path
    tar_file = tarfile.TarFile.open(tar_file_path)
    tar_file.extractall(path=extract_container_dir)
    print 'extracted'

def _migrate_db():
    call_command('migrate')
    print 'db migrated'

def _capture_output(func):
    old = sys.stdout
    sys.stdout = StringIO()
    func()
    output = sys.stdout.getvalue()
    sys.stdout = old
    return output

def _get_extracted_dir(extract_container):
    for root, dirs, files in os.walk(extract_container):
        return os.path.join(root, dirs[0])

def _copy(src, dest):
    if not os.path.isdir(dest):
        shutil.copytree(src, dest)
    else:
        for f in os.listdir(src):
            src_node = os.path.join(src, f)
            dest_node = os.path.join(dest, f)
            if os.path.isfile(src_node):
                shutil.copy2(src_node, dest_node)
            else:
                _copy(src_node, dest_node)

def _restart_server():
    args = sys.argv[:]
    print 'Respawning %s' % ' '.join(args)

    args.insert(0, sys.executable)
    os.execv(sys.executable, args)