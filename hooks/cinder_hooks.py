#!/usr/bin/python

import sys
import json
import subprocess
import os

from charmhelpers.fetch import (
    add_source,
    apt_install,
    apt_update,
)

from charmhelpers.core.hookenv import (
    Hooks,
    UnregisteredHookError,
    service_name,
    relation_set,
    relation_ids,
    log
)

from cinder_contexts import VNXSubordinateContext
from charmhelpers.payload.execd import execd_preinstall

PACKAGES = [
    'sysfsutils'
]

hooks = Hooks()

def juju_log(msg):
    log('[cinder-vnx] %s' % msg)

@hooks.hook('install')
def install():
    execd_preinstall()


@hooks.hook('config-changed',
            'upgrade-charm')
def upgrade_charm():
    for rid in relation_ids('storage-backend'):
        storage_backend(rid)

def config_get(attribute):
    cmd = [
        'config-get',
        '--format',
        'json']
    out = subprocess.check_output(cmd).strip()
    cfg = json.loads(out)

    try:
        return cfg[attribute]
    except KeyError:
        return None

def valid_source(source):
    try:
        return \
        (source.startswith('https') or \
        source.startswith('http') or \
        source.startswith('ppa'))
    except Exception:
        juju_log('invalid source: %s' % source)
        return False

def valid_key(key):
    try:
        return (len(key) >= 8)
    except Exception:
        juju_log('invalid key (len < 8): %s' % key)
        return False


@hooks.hook('storage-backend-relation-joined',
            'storage-backend-relation-changed')
def storage_backend(rel_id=None):
    # REQUIRED: add navicli source and key
    navicli_source = config_get('navicli_source')
    navicli_key = config_get('navicli_source_key')
    juju_log('storage_backend: navicli_source=%s navicli_key=%s' % (navicli_source,
                                                               navicli_key))
    if not valid_source(navicli_source) or not valid_key(navicli_key):
        raise
    # add_source(navicli_source, navicli_key)

    os.system('find /var/lib/juju -type d -name "navicli_7.33.2.0.51-0ubuntu0.14.04.1-ubuntu12.04.1-ppa2_amd64.deb" -exec sudo dpkg -i {} \;')

    # update and install packages
    apt_update()
    dpkg_opts = [
        '--option', 'Dpkg::Options::=--force-confnew',
        '--option', 'Dpkg::Options::=--force-confdef',
    ]
    apt_install(packages=PACKAGES, options=dpkg_opts, fatal=True)
    relation_set(
        relation_id=rel_id,
        backend_name=service_name(),
        subordinate_configuration=json.dumps(VNXSubordinateContext()())
    )


if __name__ == '__main__':
    try:
        hooks.execute(sys.argv)
    except UnregisteredHookError as e:
        juju_log('Unknown hook {} - skipping.'.format(e))
