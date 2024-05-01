from router_manager import Router  # Importing Router class from router_manager module
from xml.etree import ElementTree as ET  # Importing ElementTree as ET for XML parsing
import time  # Importing time module for time-related operations


def parse(stats):
    """
    Parse the XML data containing memory statistics and store them in a dictionary format.

    Args:
        stats (Element): The XML element containing memory statistics.

    Returns:
        list: A list of dictionaries, each representing memory statistics for an interface.
    """
    results = []  # Store interface statistics
    for interface in stats.findall('.//{http://cisco.com/ns/yang/Cisco-IOS-XE-memory-oper}memory-statistic'):
        # Extract memory statistics from XML elements
        name = interface.find('.//{http://cisco.com/ns/yang/Cisco-IOS-XE-memory-oper}name').text
        total_memory = int(interface.find('.//{http://cisco.com/ns/yang/Cisco-IOS-XE-memory-oper}total-memory').text)
        used_memory = int(interface.find('.//{http://cisco.com/ns/yang/Cisco-IOS-XE-memory-oper}used-memory').text)
        free_memory = int(interface.find('.//{http://cisco.com/ns/yang/Cisco-IOS-XE-memory-oper}free-memory').text)
        lowest_usage = int(interface.find('.//{http://cisco.com/ns/yang/Cisco-IOS-XE-memory-oper}lowest-usage').text)
        highest_usage = int(interface.find('.//{http://cisco.com/ns/yang/Cisco-IOS-XE-memory-oper}highest-usage').text)
        memory_utilisation = (used_memory / total_memory) * 100

        # Store memory statistics in a dictionary format
        interface_stats = {
            'name': name,
            'stats': {
                'total_memory': total_memory,
                'used_memory': used_memory,
                'free_memory': free_memory,
                'lowest_usage': lowest_usage,
                'highest_usage': highest_usage,
                'memory_utilisation': float(memory_utilisation)
            }
        }
        results.append(interface_stats)
    return results


def get_memory_statistics():
    """
    Retrieve memory statistics from a router periodically and store them in InfluxDB.
    """
    try:
        # Create a router object
        router = Router("10.10.20.48", 830, "developer", "C1sco12345", "http://localhost:8086",
                        "my-super-secret-auth-token", "my-org", "network")

        # Define the XML filter to retrieve memory statistics
        data = '''
                <filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
                    <memory-statistics xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-memory-oper"/>
                </filter>
                '''
        # Retrieve memory statistics using NETCONF
        response = router.get_stats(data)

        # Parse the XML response and extract memory statistics
        result = parse(ET.fromstring(response.data_xml))

        # Store memory statistics in InfluxDB
        router.write_to_influxdb('memory_stats', 'name', result)

    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    # Execute the function to retrieve memory statistics periodically
    while True:
        get_memory_statistics()
        time.sleep(15)  # Sleep for 15 seconds before the next retrieval
