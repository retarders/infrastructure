import pulumi
import pulumi_openstack as openstack

# create internal network and subnet
network = openstack.networking.Network('retarders', admin_state_up=True)

internal = openstack.networking.Subnet(
        'internal',
        cidr='192.168.199.0/24',
        ip_version=4,
        network_id=network.id
)

# create data volume
# this volume contains stuff like maps, maven cache and plugins but ironically, not database data
data = openstack.blockstorage.Volume('data', description='maps, plugins and stuff', size=50)

# create database secgroup
database_secgroup = openstack.compute.SecGroup(
        'database',
        description='database secgroup',
        rules=[

            # allow tcp traffic on port 5432 (postgresql) from internal network
            openstack.compute.SecGroupRuleArgs(
                cidr=internal.cidr,
                from_port=5432,
                to_port=5432,
                ip_protocol='tcp'
            ),

            # allow tcp traffic on port 6379 (redis) from internal network
            openstack.compute.SecGroupRuleArgs(
                cidr=internal.cidr,
                from_port=6379,
                to_port=6379,
                ip_protocol='tcp'
            )

])

# create a database instance
# this instance hosts PostgreSQL and Redis
database = openstack.compute.Instance(
        'database',
        flavor_name='cc1.xsmall',
        image_name='Debian-10.5',
        networks=[openstack.compute.InstanceNetworkArgs(name=network.name)]
)

pulumi.export('database_ip', database.access_ip_v4)

# create craft secgroup
craft_secgroup = openstack.compute.SecGroup(
        'craft',
        description='craft secgroup',
        rules=[

            # allow tcp traffic on port 25565 (minecraft) from external network (load balancer) (hardcoded)
            openstack.compute.SecGroupRuleArgs(
                cidr='195.114.30.0/24',
                from_port=25565,
                to_port=25565,
                ip_protocol='tcp'
            )

])

# create a craft instance
# this instance hosts game servers
craft = openstack.compute.Instance(
        'craft',
        flavor_name='cc1.large',
        image_name='Debian-10.5',
        networks=[openstack.compute.InstanceNetworkArgs(name=network.name)],
        block_devices=[openstack.compute.InstanceBlockDeviceArgs(source_type='volume', uuid=data.id)]
)

pulumi.export('craft_ip', craft.access_ip_v4)
