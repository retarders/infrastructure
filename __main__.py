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

# create database secgroup
database_secgroup = openstack.compute.SecGroup(
        'database_secgroup',
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

# create port
database_port = openstack.networking.Port(
        'database',
        admin_state_up=True,
        fixed_ips=[openstack.networking.PortFixedIpArgs(ip_address='192.168.199.11', subnet_id=internal.id)],
        network_id=internal.id,
        security_group_ids=[database_secgroup.id]
)

# create a database instance
# this instance hosts PostgreSQL and Redis
database = openstack.compute.Instance(
        'database',
        flavor_name='cc1.xsmall',
        image_name='Debian-10.5',
        networks=[openstack.compute.InstanceNetworkArgs(name='internal')]
)

pulumi.export('database_ip', database.access_ip_v4)
