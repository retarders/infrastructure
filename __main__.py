import pulumi
import pulumi_openstack as openstack
import random
import string

IMAGE = 'Debian-10.5'

def gen_password():
    """
    generates a 12 letter password using a very weird character set
    """
    return ''.join([random.choice(string.digits * 3 + string.punctuation) for _ in range(12)])

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
        image_name=IMAGE,
        networks=[openstack.compute.InstanceNetworkArgs(name=network.name)],
        admin_pass=gen_password()
)

pulumi.export('database_ip', database.access_ip_v4)

# not sure if this is secure
pulumi.export('database_password', database.admin_pass)

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
        image_name=IMAGE,
        networks=[openstack.compute.InstanceNetworkArgs(name=network.name)],
        block_devices=[

            # boot image
            openstack.compute.InstanceBlockDeviceArgs(
                uuid=openstack.images.get_image(name=IMAGE).id,
                source_type='image',
                destination_type='local',
                boot_index=0,
                delete_on_termination=True
            ),

            # data
            openstack.compute.InstanceBlockDeviceArgs(
                uuid=data.id, 
                source_type='volume',
                destination_type='volume',
                boot_index=1,
                delete_on_termination=True
            )

        ],
        admin_pass=gen_password()
)

pulumi.export('craft_ip', craft.access_ip_v4)

# not sure if this is secure
pulumi.export('craft_password', craft.admin_pass)
