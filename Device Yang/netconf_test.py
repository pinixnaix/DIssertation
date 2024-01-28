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

        cpu_usage = """
         <filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
                <cpu-usage xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-process-cpu-oper"/>
         </filter>
         
        """

        netconf_reply = m.get(filter=cpu_usage).xml
        #print(xml.dom.minidom.parseString(netconf_reply).toprettyxml())

        cpu = xmltodict.parse(netconf_reply)["rpc-reply"]["data"]["cpu-usage"]["cpu-utilization"]["cpu-usage-processes"]["cpu-usage-process"]

        display(cpu)


if __name__ == "__main__":
    run()
