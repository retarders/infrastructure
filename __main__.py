import pulumi
import pulumi_openstack as openstack

IMAGE = 'Debian-10.5'
MY_KEY = 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDDSzsSGRaP8OuHnqr7o8hviYYls4ieHQqzLn+TfezyRfTyapuD3QDZqCk4dhFjNrhpB+1pSlBZUWZqa439lNYCBp/6qSZ1Gy9/H/5Nrjeho9PYR0+/lWK4FTw1FqEPkWKX2XqR64OV60vMFe/Lav0n2ZK1dxx1Cu34lEg4BvV9bylAAhdk0pF69Tl+iSdkgHw92VQKdDvPw0Ch04Qr77KDemVG5ILiI4rgQSrQRVMdT550x9ajgnAO+meXYBHSPL2KUedaiReixPObzdOg6uvgMKY+qTCLerSAb+2ZgiMJVPunr6U9A+QfNPDv3mxgnatpDKCm2fpzvssT1ip56pFEVlqNc6cDl03hB7UlR/ZeMgj3V5b3fZwMnHZBIJTCahefIl13C9E19sJ+d450ItIqBbXk1wxtm7X0sosLgnGMvENM8thZYVqBb0DrgZrgoL8bvQ7WkAOgW7X6tQBkIAjPpkWS5GJvQOD/APrtqztC8TO83ynwUISJTyIWFOuUoUs='

# create data volume
# this volume contains stuff like maps, maven cache and plugins but ironically, not database data
data = openstack.blockstorage.Volume('data', description='maps, plugins and stuff', size=50)

# create a database instance
# this instance hosts PostgreSQL and Redis
database = openstack.compute.Instance(
        'database',
        flavor_name='cc1.xsmall',
        image_name=IMAGE,
        key_pair=MY_KEY
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

        key_pair=MY_KEY
)

pulumi.export('craft_ip', craft.access_ip_v4)
