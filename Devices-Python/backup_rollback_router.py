from router_manager import Router
import xml.etree.ElementTree as ET


def change_root(xml_string, new_root_tag):
    try:
        # Parse the XML string
        root = ET.fromstring(xml_string)
        # Modify the tag and attributes of the existing root element
        root.tag = new_root_tag
        root.attrib = {}
        # Serialize the modified XML to a string
        modified_xml = ET.tostring(root, encoding="unicode")
        print("Root element changed successfully.")
        return modified_xml
    except ET.ParseError as e:
        print("XML parsing error:", e)
    except Exception as e:
        print("Error:", e)


def run():
    router = Router("10.10.20.48", 830, "developer", "C1sco12345", "http://localhost:8086",
                    "my-super-secret-auth-token", "my-org", "network")

    print("Please enter one of the options: ")
    print("[1] - Get the running config from the router")
    print("[2] - Rollback the running config to the router")
    choice = input("option: ")
    if choice == '1':
        config = router.backup_configuration()
        router.write_to_influxdb("router_config", "running-config", config)
    elif choice == '2':
        data = router.get_config_from_influxdb()
        backup_config = change_root(data, '{urn:ietf:params:xml:ns:netconf:base:1.0}config')
        router.rollback_configuration(backup_config)
    else:
        print("Invalid choice. Please enter '1' or '2'.")


if __name__ == "__main__":
    run()
