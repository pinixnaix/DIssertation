# Import API libraries
from ncclient import manager
import xmltodict


def display(data):
    for interface in data:
        print("""Name: {}\nADMIN-STATUS: {}\nOPER-STATUS: {}\nSPEED: {}\nSTATISTICS:\n\tIN-OCTETS: {}
    IN-UNICAST-PKTS: {}\n\tIN-BROADCAST-PKTS: {}\n\tIN-MULTICAST-PKTS: {}\n\tIN-DISCARDS: {}
    IN-ERRORS: {}\n\tOUT-OCTETS: {}\n\tOUT-UNICAST-PKTS: {}\n\tOUT-BROADCAST-PKTS: {}
    OUT-MULTICAST-PKYS: {}\n\tOUT-DISCARDS: {}\n\tOUT-ERRORS: {}\n""".format(
            interface["name"], interface["admin-status"], interface["oper-status"], interface["speed"],
            interface["statistics"]["in-octets"], interface["statistics"]["in-unicast-pkts"],
            interface["statistics"]["in-broadcast-pkts"], interface["statistics"]["in-multicast-pkts"],
            interface["statistics"]["in-discards"], interface["statistics"]["in-errors"],
            interface["statistics"]["out-octets"], interface["statistics"]["out-unicast-pkts"],
            interface["statistics"]["out-broadcast-pkts"], interface["statistics"]["out-multicast-pkts"],
            interface["statistics"]["out-discards"], interface["statistics"]["out-errors"]))


def run():
    with manager.connect(
        host="sandbox-iosxe-latest-1.cisco.com",
        port=830,
        username="admin",
        password="C1sco12345",
        hostkey_verify=False
    ) as m:

        #for capability in m.server_capabilities:
         #   print(capability)

        #config = m.get_config(source="running")
        #print(config)

        interfaces_status = """
         <filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
           <interfaces-state xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces"/>
         </filter>
         
        """

        netconf_reply = m.get(filter=interfaces_status).xml

        interfaces = xmltodict.parse(netconf_reply)["rpc-reply"]["data"]["interfaces-state"]["interface"]

        display(interfaces)


if __name__ == "__main__":
    run()
