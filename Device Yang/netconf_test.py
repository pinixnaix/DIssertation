# Import API libraries
from ncclient import manager
import xml.dom.minidom
import xmltodict


def display(data):
    for interface in data:
        print("""PID: {}\nNAME: {}\nTTY: {}\nTOTAL RUN TIME: {}\nINVOCATION COUNT: {}\nAVG RUN TIME: {}
FIVE SECONDS: {}\nONE MINUTE: {}\nFIVE MINUTES: {}\n""".format(
            interface["pid"], interface["name"], interface["tty"], interface["total-run-time"],
            interface["invocation-count"], interface["avg-run-time"],interface["five-seconds"],
            interface["one-minute"], interface["five-minutes"]))


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

        hardware = """
         <filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
                 <device-hardware-data xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-device-hardware-oper"/>
         </filter>
        """

        flow_monitors = """
        <filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
                <flow-monitors xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-flow-monitor-oper"/>
        </filter>
        """

        ip_sla_stats = """
        <filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
                <ip-sla-stats xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-ip-sla-oper"/>    
        </filter>
         """

        mem_stats = """
        <filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
            <memory-statistics xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-memory-oper"/>
        </filter>
        """

        mem_usage_processes = """
        <filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
            <memory-usage-processes xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-process-memory-oper"/>
        </filter>
        """

        netconf_reply4 = m.get(filter=mem_usage_processes).xml
        print(xml.dom.minidom.parseString(netconf_reply4).toprettyxml())

        netconf_reply = m.get(filter=hardware).xml
        print(xml.dom.minidom.parseString(netconf_reply).toprettyxml())

        netconf_reply1 = m.get(filter=flow_monitors).xml
        print(xml.dom.minidom.parseString(netconf_reply1).toprettyxml())

        netconf_reply2 = m.get(filter=ip_sla_stats).xml
        print(xml.dom.minidom.parseString(netconf_reply2).toprettyxml())

        netconf_reply3 = m.get(filter=mem_stats).xml
        print(xml.dom.minidom.parseString(netconf_reply3).toprettyxml())

        #cpu = xmltodict.parse(netconf_reply)["rpc-reply"]["data"]["cpu-usage"]["cpu-utilization"]["cpu-usage-processes"]["cpu-usage-process"]

        #display(cpu)


if __name__ == "__main__":
    run()
