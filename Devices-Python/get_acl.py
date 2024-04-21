from ncclient import manager
from xml.etree import ElementTree as ET

# Define router connection parameters
router_ip = '10.10.20.48'
router_port = 830
router_username = 'developer'
router_password = 'C1sco12345'

def get_acl():
    try:
        # Connect to the router using NETCONF
        with manager.connect(host=router_ip, port=router_port, username=router_username, password=router_password, hostkey_verify=False) as m:
            # Construct XML filter to retrieve ACL data
            filter = '''
                <filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
                    <acl xmlns="http://openconfig.net/yang/acl"/>
                </filter>
            '''

            # Send NETCONF <get> operation with the filter
            response = m.get(filter)

            # Parse the XML response
            root = ET.fromstring(response.data_xml)

            # Print ACL information
            print("Access Control List (ACL):")
            for acl_entry in root.findall('.//{http://openconfig.net/yang/acl}acl'):
                acl_name = acl_entry.find('{http://openconfig.net/yang/acl}name').text
                acl_type = acl_entry.find('{http://openconfig.net/yang/acl}type').text
                print(f"ACL Name: {acl_name}, Type: {acl_type}")
                # You can add more parsing logic here to extract specific ACL rules if needed

    except Exception as e:
        print("Error:", e)

# Execute the function to retrieve and display the ACL
get_acl()
