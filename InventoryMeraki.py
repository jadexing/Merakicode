"""
It records the start time.
It gets the API key and organization ID.
It fetches the list of networks.
For each network, it retrieves the AP inventory and compiles the data into a list.
It creates a DataFrame from the compiled data and adds a total row for each column.
It exports the data to an Excel spreadsheet with a timestamped filename.
It calculates and prints the duration of the job.
In summary, this code collects and organizes data about Meraki networks and their access points, then saves the information to an Excel file.
"""

#Jamieinbox - Wi-Fi Cool Cats https://jamiegprice.substack.com/ CWNE #510

import requests
import pandas as pd
import datetime

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
    
    org_list.sort(key=lambda x: x["name"])  # Sort organizations alphabetically
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

# Function to fetch and return a sorted list of networks for a specific organization
def get_networks(api_key, org_id):
    url = f"https://api.meraki.com/api/v1/organizations/{org_id}/networks"
    headers = {"X-Cisco-Meraki-API-Key": api_key}
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    return sorted(response.json(), key=lambda x: x["name"])  # Sort networks by name

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
    start_time = datetime.datetime.now()
    
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
        ap_inventory["Total"] = sum(ap_inventory.values())  # Add total per row
        data.append({"Network Name": network_name, **ap_inventory})

    df = pd.DataFrame(data)

    # Ensure columns are sorted alphabetically, except "Network Name" and "Total"
    column_order = ["Network Name"] + sorted([col for col in df.columns if col not in ["Network Name", "Total"]]) + ["Total"]
    df = df[column_order]

    # Add a total row at the end
    total_row = df.sum(numeric_only=True, axis=0).to_dict()
    total_row["Network Name"] = "Total"
    df = pd.concat([df, pd.DataFrame([total_row])], ignore_index=True)

    # Export the data to an Excel spreadsheet
    output_file = f"meraki_ap_inventory_{start_time.strftime('%Y-%m-%d_%H-%M-%S')}.xlsx"
    df.to_excel(output_file, index=False, engine='openpyxl')

    end_time = datetime.datetime.now()
    duration_minutes = (end_time - start_time).total_seconds() / 60.0

    print(f"Data has been collected and saved to '{output_file}'.")
    print(f"Job completed in {duration_minutes:.2f} minutes.")

if __name__ == "__main__":
    main()
