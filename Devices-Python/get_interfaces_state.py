import json
from ncclient import manager
from xml.etree import ElementTree as ET


# Define router connection parameters
router_ip = '10.10.20.48'
router_port = 830
router_username = 'developer'
router_password = 'C1sco12345'


def display(stats):
    # Store interface statistics in a dictionary
    interface_stats = []
    for interface in stats.findall('.//{urn:ietf:params:xml:ns:yang:ietf-interfaces}interface'):
        name = interface.find('{urn:ietf:params:xml:ns:yang:ietf-interfaces}name').text
        admin_status = interface.find('.//{urn:ietf:params:xml:ns:yang:ietf-interfaces}admin-status').text
        oper_status = interface.find('.//{urn:ietf:params:xml:ns:yang:ietf-interfaces}oper-status').text
        speed = interface.find('.//{urn:ietf:params:xml:ns:yang:ietf-interfaces}speed').text
        in_errors = interface.find('.//{urn:ietf:params:xml:ns:yang:ietf-interfaces}in-errors').text
        in_octets = interface.find('.//{urn:ietf:params:xml:ns:yang:ietf-interfaces}in-octets').text
        in_unicast_pkts = interface.find('.//{urn:ietf:params:xml:ns:yang:ietf-interfaces}in-unicast-pkts').text
        in_broadcast_pkts = interface.find('.//{urn:ietf:params:xml:ns:yang:ietf-interfaces}in-broadcast-pkts').text
        in_multicast_pkts = interface.find('.//{urn:ietf:params:xml:ns:yang:ietf-interfaces}in-multicast-pkts').text
        in_discards = interface.find('.//{urn:ietf:params:xml:ns:yang:ietf-interfaces}in-discards').text
        out_errors = interface.find('.//{urn:ietf:params:xml:ns:yang:ietf-interfaces}out-errors').text
        out_octets = interface.find('.//{urn:ietf:params:xml:ns:yang:ietf-interfaces}out-octets').text
        out_unicast_pkts = interface.find('.//{urn:ietf:params:xml:ns:yang:ietf-interfaces}out-unicast-pkts').text
        out_broadcast_pkts = interface.find('.//{urn:ietf:params:xml:ns:yang:ietf-interfaces}out-broadcast-pkts').text
        out_multicast_pkts = interface.find('.//{urn:ietf:params:xml:ns:yang:ietf-interfaces}out-multicast-pkts').text
        out_discards = interface.find('.//{urn:ietf:params:xml:ns:yang:ietf-interfaces}out-discards').text
        stats = {'admin_status': admin_status, 'oper_status': oper_status, 'speed': speed,
                 'in_errors': in_errors, 'in_octets': in_octets, 'in_unicast_pkts': in_unicast_pkts,
                 'in_broadcast_pkts': in_broadcast_pkts, 'in_multicast_pkts': in_multicast_pkts,
                 'in_discards': in_discards, 'out_errors': out_errors, 'out_octets': out_octets,
                 'out_unicast_pkts': out_unicast_pkts, 'out_broadcast_pkts': out_broadcast_pkts,
                 'out_multicast_pkts': out_multicast_pkts, 'out_discards': out_discards,
                 'field': 'interface_stats', 'name': name, 'host': router_ip}
        interface_stats.append(stats)

    # Returns the interface stats dict in a json format
    return json.dumps(interface_stats)


def get_interface_statistics():
    # Connect to the router using NETCONF
    with manager.connect(host=router_ip,
                         port=router_port,
                         username=router_username,
                         password=router_password,
                         hostkey_verify=False) as m:
        # XML filter to retrieve interface statistics
        filter = '''
            <filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
                <interfaces-state xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces"/>
            </filter>
        '''

        # Send NETCONF <get> operation with the filter
        response = m.get(filter)

        # Parse the XML response and send to display
        print(display(ET.fromstring(response.data_xml)))


if __name__ == "__main__":
    # Execute the function to retrieve statistics from each interface
    get_interface_statistics()
