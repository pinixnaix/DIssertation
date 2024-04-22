# Import API libraries
import xmltodict
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
        filter = '''
                        <filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
                            <acl xmlns="http://openconfig.net/yang/acl"/>
                        </filter>
                    '''
        config = m.get(filter).data_xml
        print(xml.dom.minidom.parseString(config).toprettyxml())


if __name__ == "__main__":
    run()
