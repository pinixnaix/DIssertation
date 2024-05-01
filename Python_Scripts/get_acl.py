from ncclient import manager  # Importing manager from ncclient module for NETCONF operations
from xml.etree import ElementTree as ET  # Importing ElementTree as ET for XML parsing

# Define router connection parameters
router_ip = '10.10.20.48'
router_port = 830
router_username = 'developer'
router_password = 'C1sco12345'


def get_acl():
    """
    Retrieves and displays the Access Control List (ACL) from the router using NETCONF.

    Returns:
        None
    """
    try:
        # Connect to the router using NETCONF
        with manager.connect(host=router_ip, port=router_port, username=router_username, password=router_password,
                             hostkey_verify=False) as m:
            # Construct XML filter to retrieve ACL data
            filter = '''
                <filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
                    <acl xmlns="http://openconfig.net/yang/acl"/>
                </filter>
                  <filter>
    <access-lists xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-acl-oper"/>
  </filter>
            '''

            # Send NETCONF <get> operation with the filter
            response = m.get(filter)

            # Parse the XML response
            root = ET.fromstring(response.data_xml)

            # Print ACL information
            print("Access Control List (ACL):")
            for acl_set in root.findall('.//{http://openconfig.net/yang/acl}acl-set'):
                acl_name = acl_set.find('{http://openconfig.net/yang/acl}name').text
                acl_type = acl_set.find('{http://openconfig.net/yang/acl}type').text
                for acl_entries in acl_set.findall('.//{http://openconfig.net/yang/acl}acl-entry'):
                    seq_id = acl_entries.find('{http://openconfig.net/yang/acl}sequence-id').text
                for actions in acl_set.findall('.//{http://openconfig.net/yang/acl}actions'):
                    for state in actions:
                        forwarding_action = state.find('{http://openconfig.net/yang/acl}forwarding-action').text
                        break
                    break
                for transport in acl_set.findall('.//{http://openconfig.net/yang/acl}transport'):
                    for state in transport:
                        source_port = state.find('{http://openconfig.net/yang/acl}source-port').text
                        destination_port = state.find('{http://openconfig.net/yang/acl}destination-port').text
                        break
                    break
                for ip in acl_set.findall('.//{http://openconfig.net/yang/acl}ipv4'):
                    for state in ip:
                        try:
                            destination_address = state.find('{http://openconfig.net/yang/acl}destination-address').text
                        except Exception as e:
                            pass
                        try:
                            source_address = state.find('{http://openconfig.net/yang/acl}source-address').text
                        except Exception as e:
                            pass
                        try:
                            protocol = state.find('{http://openconfig.net/yang/acl}protocol').text
                        except Exception as e:
                            pass
                        break
                    break
                print(f"Extended " + ("IP" if acl_type == "ACL_IPV4" else "IPV6") + f" access list {acl_name}")
                if source_address is not None:
                    print(f"\t{seq_id} " + ("permit " if forwarding_action == "ACCEPT" else "deny") +
                          f"{protocol.split(':')[1].lower()} {source_address} {destination_port.lower()}")
                    source_address, destination_address = None, None
                    source_port, destination_port = None, None
                else:
                    print(f"\t{seq_id} " + ("permit " if forwarding_action == "ACCEPT" else "deny ") +
                          f"{protocol.split(':')[1].lower()} {destination_port.lower()} {source_port.lower()}"
                          f" {destination_address.split('/')[0]}")
                    source_address, destination_address = None, None
                    source_port, destination_port = None, None

    except Exception as e:
        print("Error:", e)


# Execute the function to retrieve and display the ACL
get_acl()
