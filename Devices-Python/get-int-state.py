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
        interfaces_status = """
                   <filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
             <interfaces-state xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
                        <interface>
                            <name>GigabitEthernet2</name>
                            <admin-status></admin-status>
				            <oper-status></oper-status>
                        </interface>
                    </interfaces-state>
         </filter>
                 """
        netconf_reply = m.get(filter=interfaces_status)

        print(xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml())


if __name__ == "__main__":
    run()
