from azure.identity import DefaultAzureCredential
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.compute import ComputeManagementClient

def create_public_ip():
    client = NetworkManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id="fbd2d30c-b959-465b-9e85-38c1dcfc921f",
    )

    response = client.public_ip_addresses.begin_create_or_update(
        resource_group_name="lab4cc",
        public_ip_address_name="ip4",
        parameters={
            "location": "westeurope",
            "properties": {
                "idleTimeoutInMinutes": 10,
                "publicIPAddressVersion": "IPv4",
                "publicIPAllocationMethod": "Static",
            },
            "sku": {"name": "Standard", "tier": "Global"},
        },
    ).result()
    print("Public IP created:", response.id)

def create_network_interface():
    client = NetworkManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id="fbd2d30c-b959-465b-9e85-38c1dcfc921f",
    )

    response = client.network_interfaces.begin_create_or_update(
        resource_group_name="lab4cc",
        network_interface_name="nic4",
        parameters={
            "location": "westeurope",
            "properties": {
                "disableTcpStateTracking": True,
                "enableAcceleratedNetworking": True,
                "ipConfigurations": [
                    {
                        "name": "ipconfig1",
                        "properties": {
                            "publicIPAddress": {
                                "id": "/subscriptions/fbd2d30c-b959-465b-9e85-38c1dcfc921f/resourceGroups/lab4cc/providers/Microsoft.Network/publicIPAddresses/ip4"
                            },
                            "subnet": {
                                "id": "/subscriptions/fbd2d30c-b959-465b-9e85-38c1dcfc921f/resourceGroups/lab4cc/providers/Microsoft.Network/virtualNetworks/net4/subnets/default"
                            },
                        },
                    }
                ],
            },
        },
    ).result()
    print("Network Interface created:", response.id)

def create_virtual_machine():
    client = ComputeManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id="fbd2d30c-b959-465b-9e85-38c1dcfc921f",
    )

    response = client.virtual_machines.begin_create_or_update(
        resource_group_name="lab4cc",
        vm_name="vm4",
        parameters={
            "location": "westeurope",
            "properties": {
                "hardwareProfile": {"vmSize": "Standard_D1_v2"},
                "networkProfile": {
                    "networkInterfaces": [
                        {
                            "id": "/subscriptions/fbd2d30c-b959-465b-9e85-38c1dcfc921f/resourceGroups/lab4cc/providers/Microsoft.Network/networkInterfaces/nic4",
                            "properties": {"primary": True},
                        }
                    ]
                },
                "osProfile": {
                    "adminPassword": "secret",
                    "adminUsername": "colin",
                    "computerName": "vm4",
                },
                "storageProfile": {
                    "osDisk": {
                        "caching": "ReadWrite",
                        "createOption": "FromImage",
                        "image": {
                            "uri": "http://your_existing_storage_account_name.blob.core.windows.net/your_existing_container_name/your_existing_generalized_os_image_blob_name.vhd"
                        },
                        "name": "vm4osdisk",
                        "osType": "Windows",
                        "vhd": {
                            "uri": "http://your_existing_storage_account_name.blob.core.windows.net/your_existing_container_name/vm4Disk.vhd"
                        },
                    }
                },
            },
        },
    ).result()
    print("Virtual Machine created:", response.id)

if __name__ == "__main__":
    create_public_ip()
    create_network_interface()
    create_virtual_machine()
