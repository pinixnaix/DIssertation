from router_manager import Router
from xml.etree import ElementTree as ET
import time


def parse(stats):
    # Store interface statistics in a dictionary
    results = []
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
        interface_stats = {'name': name,
                           'stats': {
                               'admin_status': float(1) if admin_status == 'up' else float(0),
                               'oper_status': 1 if oper_status == 'up' else 0,
                               'speed': float(speed), 'in_errors': float(in_errors), 'in_octets': float(in_octets),
                               'in_unicast_pkts': float(in_unicast_pkts), 'in_broadcast_pkts': float(in_broadcast_pkts),
                               'in_multicast_pkts': float(in_multicast_pkts), 'in_discards': float(in_discards),
                               'out_errors': float(out_errors), 'out_octets': float(out_octets),
                               'out_unicast_pkts': float(out_unicast_pkts), 'out_broadcast_pkts': float(out_broadcast_pkts),
                               'out_multicast_pkts': float(out_multicast_pkts), 'out_discards': float(out_discards)}}
        results.append(interface_stats)
    return results


def get_interface_statistics():
    try:
        router = Router("10.10.20.48", 830, "developer", "C1sco12345", "http://localhost:8086",
                        "my-super-secret-auth-token",
                        "my-org", "network")
        data = '''
                                    <filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
                                        <interfaces-state xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces"/>
                                    </filter>
                                '''
        # Send NETCONF <get> operation with the filter
        response = router.get_stats(data)

        result = parse(ET.fromstring(response.data_xml))
        # Parse the XML response and send to influxdb
        router.write_to_influxdb('interface_stats', 'name', result)

    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    # Execute the function to retrieve interface statistics
    while True:
        get_interface_statistics()
        time.sleep(5)
