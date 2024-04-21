import xml.dom.minidom
from ncclient import manager

router_ip = '10.10.20.48'  # Specify the IP address of the router
router_port = 830  # Specify the NETCONF port (usually 830)
router_username = 'developer'  # Specify the router's username
router_password = 'C1sco12345'  # Specify the router's password

# Connect to the router using NETCONF
with manager.connect(host=router_ip, port=router_port, username=router_username, password=router_password,
                     hostkey_verify=False) as m:
    # Retrieve the ACL data using NETCONF
    netconf_reply = m.get(filter=('subtree',
                             '<acl xmlns="http://openconfig.net/yang/acl"/>')).data_xml
    print(xml.dom.minidom.parseString(netconf_reply).toprettyxml())
