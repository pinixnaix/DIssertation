from ncclient import manager
from xml.etree import ElementTree as ET
import time

# Define router connection parameters
router_ip = '10.10.20.48'
router_port = 830
router_username = 'developer'
router_password = 'C1sco12345'

# Define time interval for bandwidth calculation (in seconds)
interval = 60


def calculate_bandwidth(previous_stats, current_stats, interval):
    # Calculate difference in octets for inbound and outbound traffic
    in_octets_diff = int(current_stats['in_octets']) - int(previous_stats['in_octets'])
    out_octets_diff = int(current_stats['out_octets']) - int(previous_stats['out_octets'])

    # Calculate bandwidth utilization in bytes per second (Bps)
    in_bandwidth = in_octets_diff / interval
    out_bandwidth = out_octets_diff / interval

    return round(in_bandwidth, 2), round(out_bandwidth, 2)


def get_interface_statistics():
    try:
        # Connect to the router using NETCONF
        with manager.connect(host=router_ip, port=router_port, username=router_username, password=router_password,
                             hostkey_verify=False) as m:
            # XML filter to retrieve interface statistics
            filter = '''
                <filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
                    <interfaces-state xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
                        <interface>
                            <name></name>
                            <statistics>
                                <in-octets/>
                                <out-octets/>
                            </statistics>
                        </interface>
                    </interfaces-state>
                </filter>
            '''

            # Send NETCONF <get> operation with the filter
            response = m.get(filter)

            # Parse the XML response
            root = ET.fromstring(response.data_xml)

            # Store interface statistics in a dictionary
            interface_stats = {}
            for interface in root.findall('.//{urn:ietf:params:xml:ns:yang:ietf-interfaces}interface'):
                name = interface.find('{urn:ietf:params:xml:ns:yang:ietf-interfaces}name').text
                in_octets = interface.find('.//{urn:ietf:params:xml:ns:yang:ietf-interfaces}in-octets').text
                out_octets = interface.find('.//{urn:ietf:params:xml:ns:yang:ietf-interfaces}out-octets').text
                interface_stats[name] = {'in_octets': in_octets, 'out_octets': out_octets}

            # Wait for the specified interval
            time.sleep(interval)

            # Retrieve interface statistics again after the interval
            response = m.get(filter)
            root = ET.fromstring(response.data_xml)

            # Calculate bandwidth for each interface
            for interface in root.findall('.//{urn:ietf:params:xml:ns:yang:ietf-interfaces}interface'):
                name = interface.find('{urn:ietf:params:xml:ns:yang:ietf-interfaces}name').text
                current_stats = {
                    'in_octets': interface.find('.//{urn:ietf:params:xml:ns:yang:ietf-interfaces}in-octets').text,
                    'out_octets': interface.find('.//{urn:ietf:params:xml:ns:yang:ietf-interfaces}out-octets').text}
                previous_stats = interface_stats.get(name, None)
                if previous_stats:
                    in_bandwidth, out_bandwidth = calculate_bandwidth(previous_stats, current_stats, interval)
                    print(f"Interface: {name}, In Bandwidth: {in_bandwidth} Bps, Out Bandwidth: {out_bandwidth} Bps")

    except Exception as e:
        print("Error:", e)


# Execute the function to retrieve and calculate interface bandwidth
get_interface_statistics()
