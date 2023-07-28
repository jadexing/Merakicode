# Merakicode
Code for Meraki Wi-Fi

"""
Meraki Unique Client Count Script

This Python script interacts with the Cisco Meraki Dashboard API to retrieve the unique client count for each network
associated with a specific organization. The script prompts the user to provide the Meraki API key and organization
number, and then lists the networks associated with the organization. The user can choose to see the unique client count
for a specific network or for all networks. The script uses proper request throttling and pagination to collect all data
and displays the unique client count per network.

Make sure you have the 'requests' library installed. You can install it using 'pip install requests'.

Author: This was made with chat iterations by Jamie G. Price (Wi-Fi Cool Cats) with ChatGPT
"""

