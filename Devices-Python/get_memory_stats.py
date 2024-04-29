import time
from router_manager import Router
from xml.etree import ElementTree as ET


def parse(stats):
    # Store interface statistics in a dictionary
    results = []
    for interface in stats.findall('.//{http://cisco.com/ns/yang/Cisco-IOS-XE-memory-oper}memory-statistic'):
        name = interface.find('.//{http://cisco.com/ns/yang/Cisco-IOS-XE-memory-oper}name').text
        total_memory = int(interface.find('.//{http://cisco.com/ns/yang/Cisco-IOS-XE-memory-oper}total-memory').text)
        used_memory = int(interface.find('.//{http://cisco.com/ns/yang/Cisco-IOS-XE-memory-oper}used-memory').text)
        free_memory = int(interface.find('.//{http://cisco.com/ns/yang/Cisco-IOS-XE-memory-oper}free-memory').text)
        lowest_usage = int(interface.find('.//{http://cisco.com/ns/yang/Cisco-IOS-XE-memory-oper}lowest-usage').text)
        highest_usage = int(interface.find('.//{http://cisco.com/ns/yang/Cisco-IOS-XE-memory-oper}highest-usage').text)
        memory_utilisation = (used_memory / total_memory) * 100
        interface_stats = {'name': name,
                           'stats': {
                               'total_memory': total_memory,
                               'used_memory': used_memory,
                               'free_memory': free_memory,
                               'lowest_usage': lowest_usage,
                               'highest_usage': highest_usage,
                               'memory_utilisation': float(memory_utilisation)}}
        results.append(interface_stats)
    return results


def get_memory_statistics():
    try:
        router = Router("10.10.20.48", 830, "developer", "C1sco12345", "http://localhost:8086",
                        "my-super-secret-auth-token",
                        "my-org", "network")
        data = '''
                             <filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
                                    <memory-statistics xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-memory-oper"/>
                             </filter>
                                   '''
        # retrieves the statistics from the router with the filter: data
        response = router.get_stats(data)
        
        result = parse(ET.fromstring(response.data_xml))
        # Parse the XML response and send to influxdb
        router.write_to_influxdb('memory_stats', 'name', result)

    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    # Execute the function to retrieve interface statistics
    while True:
        get_memory_statistics()
        time.sleep(15)
