# Importing necessary libraries for interacting with the NETCONF device and parsing XML
from ncclient import manager
import xml.dom.minidom


def run():
    # Establishing a NETCONF connection to the device
    with manager.connect(
            host="10.10.20.48",
            port=830,
            username="developer",
            password="C1sco12345",
            hostkey_verify=False
    ) as m:
        # Defining a filter to retrieve interface status information from the device
        interfaces_status = """
                   <filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
             <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
                </interfaces>
         </filter>
                 """
        # Sending a NETCONF get request to retrieve interface status information
        netconf_reply = m.get(filter=interfaces_status)

        # Parsing the NETCONF reply XML and printing it in a readable format
        print(xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml())


if __name__ == "__main__":
    # Calling the run function when the script is executed directly
    run()
