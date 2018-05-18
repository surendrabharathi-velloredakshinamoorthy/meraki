import requests
import json
import texttable as tt

api_key = "34f00cc84b8219c52bb911c80ddfde63df065082"
base_url = "https://dashboard.meraki.com/api/v0/organizations/"
device_url = "https://dashboard.meraki.com/api/v0/networks/"

print("1.Create a network device")
print("2.List network devices")
print("3.Delete a network")
print("4.Add a device in a network")
print("5.List all devices in a network")
operation_input = int(input("Enter your operation \n"))

# Headers
headers1 = {'X-Cisco-Meraki-API-Key': api_key, 'Content-Type': "application/json"}

# Get Organisation Id
get_org_id = requests.get(base_url, headers=headers1)
get_org_id = get_org_id.json()[0]
org_id = str(get_org_id['id'])

# custom_url
url = base_url + org_id + "/networks/"


# List the network in an organisation
def list_network():
    get_requests = requests.get(url, headers=headers1)
    get_requests = get_requests.json()
    display_network(get_requests)


# Display in Table
def display_network(list_json):
    tab = tt.Texttable()
    headings = ['id', 'organization Id', 'name', 'timeZone', 'tags', 'type']
    net_id = []
    organizationId = []
    name = []
    timeZone = []
    tags = []
    net_type = []
    tab.header(headings)
    for item in list_json:
        net_id.append(item['id'])
        organizationId.append(org_id)
        name.append(item['name'])
        timeZone.append(item['timeZone'])
        tags.append(item['tags'])
        net_type.append(item['type'])

    for row in zip(net_id, organizationId, name, timeZone, tags, net_type):
        tab.add_row(row)

    s = tab.draw()
    print(s)


# display devices
def display_device(list_json):
    tab = tt.Texttable()
    headings = ['serial', 'mac', 'lattitude', 'longitude', 'address', 'name', 'Network id']
    serial = []
    mac = []
    lat = []
    lng = []
    address = []
    name = []
    networkId = []
    tab.header(headings)
    for item in list_json:
        serial.append(item['serial'])
        mac.append(item['mac'])
        lat.append(item['lat'])
        lng.append(item['lng'])
        address.append(item['address'])
        name.append(item['name'])
        networkId.append(item['networkId'])

    for row in zip(serial, mac, lat, lng, address, name,networkId):
        tab.add_row(row)

    devices_table = tab.draw()
    print(devices_table)


# Create a new network in an organisation
def create_network(name, network_type, network_tags):
    network_obj = {
        "name": name,
        "timeZone": "Europe/Amsterdam",
        "tags": network_tags,
        "type": network_type
    }

    response = requests.post(url, json.dumps(network_obj), headers=headers1)
    response = response.json()
    print(response)


# Delete a existing network
def delete_network(delete_name):
    get_values = requests.get(url, headers=headers1)
    get_values = get_values.json()
    return_element = next(item for item in get_values if item["name"] == delete_name)
    return_id = return_element['id']
    url_delete = url + return_id
    response = requests.delete(url_delete, headers=headers1)
    print(response)


# List all devices in a network
def list_devices(network_name):
    get_devices = requests.get(url, headers=headers1)
    get_devices = get_devices.json()
    return_element = next(item for item in get_devices if item["name"] == network_name)
    return_id = return_element['id']
    url_devices = device_url + return_id + "/devices"
    get_devices = requests.get(url_devices, headers=headers1)
    get_devices = get_devices.json()
    display_device(get_devices)


# Main
if operation_input == 1:
    name = input("Enter the name of the network \n")
    network_type = input("Enter the type of network \n")
    network_tags = input("Enter tags \n")
    create_network(name, network_type, network_tags)
elif operation_input == 2:
    list_network()
elif operation_input == 3:
    delete_name = input("Name to delete: \n")
    delete_network(delete_name)
elif operation_input == 5:
    network_name = input("Name the network \n")
    list_devices(network_name)


