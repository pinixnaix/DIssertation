# Import API libraries
from ncclient import manager
import xmltodict


def display(data):
    for interface in data:
        print("""NAME: {}\nTOTAL-MEMORY: {} bytes\nUSED-MEMORY: {} bytes\nFREE-MEMORY: {} bytes
LOWEST-USAGE: {} bytes\nHIGHEST-USAGE: {} bytes\n""".format(
            interface["name"], interface["total-memory"], interface["used-memory"], interface["free-memory"],
            interface["lowest-usage"], interface["highest-usage"]))


def run():
    with manager.connect(
        host="devnetsandboxiosxe.cisco.com",
        port=830,
        username="admin",
        password="C1sco12345",
        hostkey_verify=False
    ) as m:
        mem_stats = """
        <filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
            <memory-statistics xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-memory-oper"/>
        </filter>
        """

        netconf_reply = m.get(filter=mem_stats).xml

        mem = xmltodict.parse(netconf_reply)["rpc-reply"]["data"]["memory-statistics"]["memory-statistic"]
        display(mem)


if __name__ == "__main__":
    run()
