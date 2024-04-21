# Import API libraries
from ncclient import manager


def run():
    with manager.connect(
            host="devnetsandboxiosxe.cisco.com",
            port=830,
            username="admin",
            password="C1sco12345",
            hostkey_verify=False
    ) as m:
        interfaces_status = """
         <config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
             <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
                        <interface>
                            <name>GigabitEthernet2</name>
                            
                        </interface>
                    </interfaces>
         </config>
        """


        netconf_reply = m.edit_config(target="running", config=interfaces_status)

    if netconf_reply.ok is True:
        print("Interface admin status changed successfully!!")
    else:
        print("Interface admin status change not successfully!!")


if __name__ == "__main__":
    run()
