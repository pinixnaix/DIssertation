from router_manager import Router  # Importing Router class from router_manager module
import xml.etree.ElementTree as ET  # Importing ElementTree module from xml.etree as ET


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
    except ET.ParseError as e:  # Handling XML parsing errors
        print("XML parsing error:", e)
    except Exception as e:  # Handling other exceptions
        print("Error:", e)


def run():
    # Creating a Router instance with specified parameters
    router = Router("10.10.20.48", 830, "developer", "C1sco12345", "http://localhost:8086",
                    "my-super-secret-auth-token", "my-org", "network")

    # Displaying options to the user
    print("Please enter one of the options: ")
    print("[1] - Get the running config from the router")
    print("[2] - Rollback the running config to the router")
    choice = input("option: ")  # Getting user's choice

    if choice == '1':  # If user chooses option 1
        # Getting the running configuration from the router
        config = router.backup_configuration()
        # Writing the running configuration to InfluxDB
        router.write_to_influxdb("router_config", "running-config", config)

    elif choice == '2':  # If user chooses option 2
        # Getting configuration data from InfluxDB
        data = router.get_config_from_influxdb()
        # Changing the root element tag of the XML data
        backup_config = change_root(data, '{urn:ietf:params:xml:ns:netconf:base:1.0}config')
        # Rolling back the configuration on the router
        router.rollback_configuration(backup_config)

    else:  # If user chooses an invalid option
        print("Invalid choice. Please enter '1' or '2'.")


if __name__ == "__main__":
    run()  # Running the main function
