"""
This script performs several operations on Cisco Meraki devices, primarily related to device claiming and updating metadata for networks and devices. It uses the following Meraki API endpoints:

GET /organizations: Retrieves a list of organizations the API key has access to (get_orgs function).
GET /organizations/{organizationId}/networks: Retrieves all networks within a specified organization (get_networks function).
POST /networks/{network_id}/devices/claim: Claims devices to a specific network based on serial numbers (claim_device function).
PUT /devices/{serial}: Updates metadata for a specified device, such as the device name, tags, address, and notes (update_device function).
GET /organizations/{organizationId}/configTemplates: Retrieves configuration templates for the specified organization (get_templates function).
POST /networks/{networkId}/bind: Binds a network configuration template to a network (bind_template function).
PUT /networks/{networkId}: Updates network metadata, specifically the network tags (update_network function).
POST /organizations/{organizationId}/networks: Creates a new network in the specified organization (create_network function).

What the Script Does
Retrieve Organization and Network Data: It retrieves organizations and networks available to the API key and targets a specific organization..
Create New Networks if Necessary: If a network specified in the CSV file doesn’t exist, it creates that network.
Claim Devices: Claims devices to specific networks based on serial numbers provided in the CSV file.
Update Network and Device Metadata: Adds metadata (e.g., tags, name, address, notes) to networks and devices.
Apply Templates: Associates configuration templates to new networks if they are specified.

"""

'''Script to claim and add metadata to claimed devices'''
import csv
import json
import time
import requests
import urllib3
import re
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

##Define API key for access to meraki

headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "X-Cisco-Meraki-API-Key": 'Place API Key here, Place API Key here, Place API Key here, Place API key here.'
}

def get_orgs():
    '''Returns all orgs'''
    url = 'https://api.meraki.com/api/v1/organizations'
    response_code = requests.get(url, headers=headers, verify=False)
    if response_code.status_code == 200:
        orgs = json.loads(response_code.text)
    elif response_code.status_code == 429:
        time.sleep(int(response_code.headers["Retry-After"]))
        response_code = requests.get(url, headers=headers, verify=False)
        orgs = json.loads(response_code.text)
    else:
        print(response_code.text)

    return orgs

def get_networks(organizationId):
    '''Return all networks in a given org'''
    url = f'https://api.meraki.com/api/v1/organizations/{organizationId}/networks'
    response_code = requests.get(url, headers=headers, verify=False)
    if response_code.status_code == 200:
        networks = json.loads(response_code.text)
    elif response_code.status_code == 429:
        time.sleep(int(response_code.headers["Retry-After"]))
        response_code = requests.get(url, headers=headers, verify=False)
        networks = json.loads(response_code.text)
    else:
        print(response_code.text)

    return networks

def claim_device(network_id,serials):
    '''Claim a device into a network with given serial num'''
    url = f'https://api.meraki.com/api/v1/networks/{network_id}/devices/claim'
    payload = {
        'serials':serials
    }

    response_code = requests.post(url=url,headers=headers,data=json.dumps(payload))
    if response_code.status_code == 200:
        return response_code
    elif response_code.status_code == 429:
        time.sleep(int(response_code.headers["Retry-After"]))
        response_code = requests.post(url=url,headers=headers,data=json.dumps(payload))
        return response_code
    elif response_code.status_code == 400: ###############
        claimed_devices = []
        error_devices = json.loads(response_code.text)
        for device in error_devices['errors']:
            claimed_devices.append((re.search(r'serial\s+(\S+)',device).group(1)))

        for claimed_device in claimed_devices:
            for serial in serials:
                if claimed_device == serial:
                    serials.pop(serials.index(serial))

        payload = {
        'serials':serials
        }
        response_code = requests.post(url=url,headers=headers,data=json.dumps(payload))
        return response_code
    else:
        print(response_code.text)
        return response_code

def update_device(device):
    '''Claim a device into a network with given serial num'''
    url = f'https://api.meraki.com/api/v1/devices/{device["serial"]}'
    payload = {
        'name': device['name'],
        'tags': device['tags'],
        'address': device['address'],
        'notes': device['notes']
    }
    response_code = requests.put(url, headers=headers, data=json.dumps(payload),verify=False)
    if response_code.status_code == 200:
        return response_code.text
    elif response_code.status_code == 429:
        time.sleep(int(response_code.headers["Retry-After"]))
        response_code = requests.put(url, headers=headers, data=json.dumps(payload),verify=False)
        return response_code.text
    else:
        print(response_code.text)
        return response_code.text

def get_templates(organizationId):
    '''Get all the organization templates'''
    url = f'https://api.meraki.com/api/v1/organizations/{organizationId}/configTemplates'
    response_code = requests.get(url, headers=headers,verify=False)
    if response_code.status_code == 200:
        return json.loads(response_code.text)
    elif response_code.status_code == 429:
        time.sleep(int(response_code.headers["Retry-After"]))
        response_code = requests.get(url=url,headers=headers,verify=False)
        return json.loads(response_code.text)
    else:
        print(response_code.text)
        return json.loads(response_code.text)

def bind_template(networkId,template_id):
    '''Bind a network template to a network'''
    url = f'https://api.meraki.com/api/v1/networks/{networkId}/bind'
    payload = {
        "configTemplateId": template_id,
        "autoBind": False
    }
    response_code = requests.post(url, headers=headers, data=json.dumps(payload),verify=False)
    if response_code.status_code == 200:
        return response_code.text
    elif response_code.status_code == 429:
        time.sleep(int(response_code.headers["Retry-After"]))
        response_code = requests.post(url=url,headers=headers,data=json.dumps(payload))
        return response_code.text
    else:
        print(response_code.text)
        return response_code.text

def update_network(network,device):
    '''Add Network Tags to network'''
    url = f'https://api.meraki.com/api/v1/networks/{network["id"]}'
    payload = {
        'tags': device['network tags']
    }
    response_code = requests.put(url, headers=headers, data=json.dumps(payload),verify=False)
    if response_code.status_code == 200:
        return response_code.text
    elif response_code.status_code == 429:
        time.sleep(int(response_code.headers["Retry-After"]))
        response_code = requests.put(url, headers=headers, data=json.dumps(payload),verify=False)
        return response_code.text
    else:
        print(response_code.text)
        return response_code.text

def create_network(organizationId,network_name):
    '''Function to create a new network'''
    url = f'https://api.meraki.com/api/v1/organizations/{organizationId}/networks'
    payload = {'name':network_name,'productTypes': ['wireless']}
    response_code = requests.post(url, headers=headers, data=json.dumps(payload),verify=False)
    if response_code.status_code == 201:
        return response_code.text
    elif response_code.status_code == 429:
        time.sleep(int(response_code.headers["Retry-After"]))
        response_code = requests.post(url=url,headers=headers,data=json.dumps(payload))
        return response_code.text
    else:
        print(response_code.text)
        return response_code.text

def open_file(filename):
    '''Open a file for reading'''
    raw_file = open(filename, mode = 'r', encoding='utf-8')
    csv_reader = csv.DictReader(raw_file)
    return csv_reader

def open_csv():
    '''Pass raw file through CSV and assign rows/colums to a dictionary'''
    #Define variables
    csv_list = []
    #prompt user for csv filename
    filename = str(input("Enter the name of the csv file. Include file extension.:\n"))
    #Open CSV
    csv_reader = open_file(filename)
    #Assign CSV to a dict
    for row in csv_reader:
        csv_dict = {
            'Network Name':row['Network name'],
            'serial':row['Serial'],
            'network tags':row['Network tags'].replace(' ','').split('.'),
            'name':row['Name'],
            'tags':row['Tags'].replace(' ','').split('.'),
            'address':row['Address'],
            'notes': row['Notes']
        }
        csv_list.append(csv_dict)
    return csv_list

def main():
    '''Main function used to call all sub functions and passed looped data through each function'''
    #Declare some variables
    network_id = {}
    network_names = []
    serials = []

    #Get the orgs
    orgs = get_orgs()
    for org in orgs:
        if org['name'] == 'University of Colorado Denver':
            organizationId = org['id']
    networks = get_networks(organizationId)
    #Populate dummy list for fast checking later
    for network in networks:
        network_names.append(network['name'])

    #Get list of existing templates
    templates = get_templates(organizationId)

    devices = open_csv()
    for device in devices:
        #Check if the network exists, if not create it.
        if not network_names.count(device['Network Name']):
            network = json.loads(create_network(organizationId,device['Network Name']))
            network_names.append(network['name'])
            networks.append(network)
            #Prompt user for template name and associate to newly created network
            template_name = str(input(f"Creating new network {network['name']}. Enter the template name to bind to this network:\n"))
            for template in templates:
                if template['name'] == template_name:
                    bind_template(network['id'],template['id'])
            #Update the network tags for the newly created network
            update_network(network,device)

        #Check if a network id has already been set, if not set it.
        if not network_id:
            for network in networks:
                if network['name'] == device['Network Name']:
                    network_id = network
        #If there is a new Network lets claim the devices and get a new networkId
        elif device['Network Name'] != network_id['name']:
            #Claim the serials in the list before changing network
            if len(serials) > 0:
                claim_device(network_id['id'],serials)
                #Clear serials list
                serials = []
            for network in networks:
                if network['name'] == device['Network Name']:
                    network_id = network
        serials.append(device['serial'])
        #Add the network tags for an existing network
        update_network(network_id,device)

    #Claim the serials in the list - there was only 1 network in the file
    if len(serials) > 0:
        claim_device(network_id['id'],serials)
    
    #Add metadata to the devices
    for device in devices:
        update_device(device)

if __name__ == '__main__':
    main()
