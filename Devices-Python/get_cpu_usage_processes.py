# Import API libraries
from ncclient import manager
import xml.dom.minidom


def run():
    with manager.connect(
            host="10.10.20.48",
            port=830,
            username="developer",
            password="C1sco12345",
            hostkey_verify=False
    ) as m:
        cpu_usage = """
         <filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
                <components xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-platform-oper"/>
         </filter>

        """

        netconf_reply = m.get(filter=cpu_usage).data_xml
        print(xml.dom.minidom.parseString(netconf_reply).toprettyxml())

if __name__ == "__main__":
    run()
