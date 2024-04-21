from ncclient import manager
from xml.etree import ElementTree as ET

# Define router connection parameters
router_ip = '10.10.20.48'
router_port = 830
router_username = 'developer'
router_password = 'C1sco12345'

def get_routing_table():
    try:
        # Connect to the router using NETCONF
        with manager.connect(host=router_ip, port=router_port, username=router_username, password=router_password, hostkey_verify=False) as m:
            # Construct XML filter to retrieve IP routing table
            filter = '''
                <filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
                    <routing-state xmlns="urn:ietf:params:xml:ns:yang:ietf-routing">
                        <routing-instance>
                            <name>default</name>
                            <ribs>
                                <rib>
                                    <name>ipv4-default</name>
                                    <address-family xmlns:rt="urn:ietf:params:xml:ns:yang:ietf-routing">rt:ipv4</address-family>
                                    <routes>
                                        <route>
                                            <destination-prefix/>
                                            <next-hop>
                                                <outgoing-interface/>
                                            </next-hop>
                                            <source-protocol/>
                                            <active/>
                                            <last-updated/>
                                        </route>
                                    </routes>
                                </rib>
                            </ribs>
                        </routing-instance>
                    </routing-state>
                </filter>
            '''

            # Send NETCONF <get> operation with the filter
            response = m.get(filter)

            # Parse the XML response
            root = ET.fromstring(response.data_xml)

            # Print routing table entries
            print("Routing Table:")
            for route in root.findall('.//{urn:ietf:params:xml:ns:yang:ietf-routing}route'):
                destination_prefix = route.find('{urn:ietf:params:xml:ns:yang:ietf-routing}destination-prefix').text
                next_hop = route.find('.//{urn:ietf:params:xml:ns:yang:ietf-routing}next-hop').find('{urn:ietf:params:xml:ns:yang:ietf-routing}outgoing-interface').text
                print(f"Destination: {destination_prefix}, Next Hop: {next_hop}")

    except Exception as e:
        print("Error:", e)

# Execute the function to retrieve and display the routing table
get_routing_table()
