# Import API libraries
from ncclient import manager
import xml.dom.minidom

def run():
    with manager.connect(
            host="sandbox-iosxe-latest-1.cisco.com",
            port=830,
            username="admin",
            password="C1sco12345",
            hostkey_verify=False
    ) as m:
        config = m.get_config(source="running").xml
        print(xml.dom.minidom.parseString(config).toprettyxml())


if __name__ == "__main__":
    run()
