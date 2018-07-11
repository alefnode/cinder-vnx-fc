from charmhelpers.core.hookenv import (
    config,
    service_name
)

from charmhelpers.contrib.openstack.context import (
    OSContextGenerator,
)


class VNXIncompleteConfiguration(Exception):
    pass


class VNXSubordinateContext(OSContextGenerator):
    interfaces = ['emc-vnx']

    _config_keys = [
        'storage_vnx_pool_name',
        'san_ip',
        'san_secondary_ip',
        'san_login',
        'san_password',
        'storage_vnx_authentication_type',
        'default_timeout',
        'destroy_empty_storage_group',
        'initiator_auto_registration',
    ]

    def __call__(self):
        ctxt = []
        missing = []
        for k in self._config_keys:
            if config(k):
                ctxt.append(("{}".format(k.replace('-', '_')),
                             config(k)))
            else:
                missing.append(k)
        if missing:
            raise VNXIncompleteConfiguration(
                'Missing configuration: {}.'.format(missing)
            )

        service = service_name()
        ctxt.append(('volume_backend_name', service))
        naviseccli = '/opt/Navisphere/bin/naviseccli'
        ctxt.append(('naviseccli_path', naviseccli))
        volume_driver = 'cinder.volume.drivers.dell_emc.vnx.driver.VNXDriver'
        ctxt.append(('volume_driver', volume_driver))
        storage_protocol = 'fc'
        ctxt.append(('storage_protocol', storage_protocol))
        return {
            "cinder": {
                "/etc/cinder/cinder.conf": {
                    "sections": {
                        service: ctxt,
                    },
                    'max_pool_size': 20,
                    'max_overflow': 30,
                }
            }
        }
