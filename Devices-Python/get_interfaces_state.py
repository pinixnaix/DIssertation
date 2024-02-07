# Import API libraries
from ncclient import manager
import xmltodict
import json


def display(data):

    interface_stats = []
    for interface in data:
        stats = {}
        interface_name = interface["name"].replace(" ", "_")
        stats = {
            "admin_status": 1 if interface["admin-status"]=="up" else 0,
            "operational_status": 1 if interface["oper-status"] == "up" else 0,
            "speed": int(interface["speed"]),
            "in_errors": int(interface["statistics"]["in-errors"]),
            "in_octets": int(interface["statistics"]["in-octets"]),
            "in_unicast_pkts": int(interface["statistics"]["in-unicast-pkts"]),
            "in_broadcast_pkts": int(interface["statistics"]["in-broadcast-pkts"]),
            "in_multicast_pkts": int(interface["statistics"]["in-multicast-pkts"]),
            "in_discards": int(interface["statistics"]["in-discards"]),
            "out_errors": int(interface["statistics"]["out-errors"]),
            "out_octets": int(interface["statistics"]["out-octets"]),
            "out_unicast_pkts": int(interface["statistics"]["out-unicast-pkts"]),
            "out_broadcast_pkts": int(interface["statistics"]["out-broadcast-pkts"]),
            "out_multicast_pkts": int(interface["statistics"]["out-multicast-pkts"]),
            "out_discards": int(interface["statistics"]["out-discards"]),
            "name": interface_name,
            "field": "interface_stats"
        }

        interface_stats.append(stats)
    return json.dumps(interface_stats)


def run():
    with manager.connect(
            host="devnetsandboxiosxe.cisco.com",
            port=830,
            username="admin",
            password="C1sco12345",
            hostkey_verify=False
    ) as m:
        interfaces_status = """
         <filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
           <interfaces-state xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces"/>
         </filter>

        """

        netconf_reply = m.get(filter=interfaces_status).xml

        interfaces = xmltodict.parse(netconf_reply)["rpc-reply"]["data"]["interfaces-state"]["interface"]

        print(display(interfaces))


if __name__ == "__main__":
    run()
