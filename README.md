# EMC VNX Storage Backend for Cinder

This charm provides a VNX storage backend for use with the Cinder
charm.

This is a modded charm for working with FC instead of ISCSI, even that, repository is not available in the original charm so we have to install it manually.

Note: Maybe you have to restart container where you deploy it after the installation.

## Configuration

The cinder-vnx charm has the following mandatory configuration.

1. To access the VNX array:
        san_ip
        san_login
        san_password

2. The auto registration feature is not available in Icehouse, user must provide the VNX direct driver source location to install auto registration packages.
        vnx_source
        vnx_source_key

This charm also provide configuration options for the following:
        navicli_source
        navicli_source_key
        storage_vnx_pool_name
        storage_vnx_authentication_type
        default_timeout
        destroy_empty_storage_group
        initiator_auto_registration

Add this configuration in the config.yaml file before deploying the charm.

## Usage

    juju deploy cinder
    juju deploy cinder-vnx
    juju add-relation cinder-vnx cinder

# Contact Information
Adrian Campos <adriancampos@teachelp.com>
