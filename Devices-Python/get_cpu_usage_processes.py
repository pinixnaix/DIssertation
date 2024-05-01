import time  # Importing time module for time-related operations
from router_manager import Router  # Importing Router class from router_manager module
from xml.etree import ElementTree as ET  # Importing ElementTree as ET for XML parsing


def parse(stats):
    """
    Parses CPU statistics XML and extracts relevant information.

    Args:
        stats (ElementTree.Element): Element containing CPU statistics XML data.

    Returns:
        list: List of dictionaries containing CPU statistics.
    """
    # Store cpu statistics in a dictionary
    results = []
    for interface in stats.findall('.//{http://cisco.com/ns/yang/Cisco-IOS-XE-process-cpu-oper}cpu-utilization'):
        five_seconds = float(interface[0].text)  # busy percentage in the last 5 seconds
        five_seconds_intr = float(interface[1].text)  # interrupt busy percentage in the last 5 seconds
        one_minute = float(interface[2].text)  # busy percentage in the last 1 minute
        five_minutes = float(interface[3].text)  # busy percentage in the last 5 minutes

        interface_stats = {'name': 'cpu',
                           'stats': {
                               'five_seconds': five_seconds,
                               'five_seconds_intr': five_seconds_intr,
                               'one_minute': one_minute,
                               'five_minutes': five_minutes}}
        results.append(interface_stats)
    return results


def get_memory_statistics():
    """
    Retrieves CPU statistics from the router and sends them to InfluxDB.
    """
    try:
        router = Router("10.10.20.48", 830, "developer", "C1sco12345", "http://localhost:8086",
                        "my-super-secret-auth-token",
                        "my-org", "network")
        data = """
         <filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
                <cpu-usage xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-process-cpu-oper"/>
         </filter>

        """

        # retrieves the statistics from the router with the filter: data
        response = router.get_stats(data)

        result = parse(ET.fromstring(response.data_xml))
        # Parse the XML response and send to influxdb
        router.write_to_influxdb('cpu_stats', 'name', result)

    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    # Execute the function to retrieve interface statistics periodically
    while True:
        get_memory_statistics()
        time.sleep(15)  # Wait for 15 seconds before retrieving data again
