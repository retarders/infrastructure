import pulumi
import pulumi_openstack as openstack

IMAGE = 'Debian-10.5'

# create data volume
# this volume contains stuff like maps, maven cache and plugins but ironically, not database data
data = openstack.blockstorage.Volume('data', description='maps, plugins and stuff', size=50)

# create a database instance
# this instance hosts PostgreSQL and Redis
database = openstack.compute.Instance(
        'database',
        flavor_name='cc1.xsmall',
        image_name=IMAGE,
        key_pair='me'
)

pulumi.export('database_ip', database.access_ip_v4)

# create a craft instance
# this instance hosts game servers
craft = openstack.compute.Instance(
        'craft',
        flavor_name='cc1.large',
        image_name=IMAGE,
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

        key_pair='me'
)

pulumi.export('craft_ip', craft.access_ip_v4)
