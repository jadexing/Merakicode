import requests
import pandas as pd

# Function to prompt the user for their Meraki API key
def get_api_key():
    return input("Please enter your Meraki API key: ")

# Function to fetch the list of organizations and select one if there's only one
def get_org_number(api_key):
    url = "https://api.meraki.com/api/v1/organizations"
    headers = {"X-Cisco-Meraki-API-Key": api_key}
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    org_list = response.json()
    
    if len(org_list) == 1:
        print(f"Automatically selecting organization: {org_list[0]['name']}")
        return org_list[0]['id']
    
    print("Organizations:")
    for i, org in enumerate(org_list):
        print(f"{i + 1}. {org['name']}")
    
    while True:
        try:
            org_index = int(input("Please enter the number of the organization you want to use: ")) - 1
            if 0 <= org_index < len(org_list):
                return org_list[org_index]['id']
            else:
                print("Invalid input. Please enter a valid organization number.")
        except ValueError:
            print("Invalid input. Please enter a valid organization number.")

# Function to fetch the list of networks for a specific organization
def get_networks(api_key, org_id):
    url = f"https://api.meraki.com/api/v1/organizations/{org_id}/networks"
    headers = {"X-Cisco-Meraki-API-Key": api_key}
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    return response.json()

# Function to get the inventory count of Access Points for a network
def get_ap_inventory(api_key, network_id):
    url = f"https://api.meraki.com/api/v1/networks/{network_id}/devices"
    headers = {"X-Cisco-Meraki-API-Key": api_key}
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    inventory = response.json()
    ap_types = {}
    
    for device in inventory:
        ap_model = device["model"]
        if ap_model.startswith("MR") or ap_model.startswith("CW"):
            ap_types[ap_model] = ap_types.get(ap_model, 0) + 1
    
    return ap_types

def main():
    api_key = get_api_key()
    org_id = get_org_number(api_key)
    
    print("Please wait while gathering data...")
    
    try:
        networks = get_networks(api_key, org_id)
    except requests.exceptions.HTTPError as e:
        print(f"Error: {e.response.text}")
        return
    
    data = []
    for network in networks:
        network_name = network["name"]
        network_id = network["id"]
        ap_inventory = get_ap_inventory(api_key, network_id)
        
        data.append({"Network Name": network_name, **ap_inventory})
    
    df = pd.DataFrame(data)
    
    # Add a row for the total of each column
    df.loc['Total'] = df.sum(numeric_only=True, axis=0)
    
    # Export the data to an Excel spreadsheet
    output_file = "meraki_ap_inventory.xlsx"
    df.to_excel(output_file, index=False, engine='openpyxl')
    
    print(f"Data has been collected and saved to '{output_file}'.")

if __name__ == "__main__":
    main()
