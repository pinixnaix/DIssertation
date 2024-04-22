import xml.etree.ElementTree as ET

def change_root(xml_file, new_root_tag, new_root_attributes):
    # Parse the XML file
    tree = ET.parse(xml_file)
    root = tree.getroot()
    print(root)
    # Create a new root element with the specified tag and attributes
    new_root = ET.Element(new_root_tag, new_root_attributes)
    print(new_root)
    # Transfer the children of the current root to the new root
    new_root.extend(root)

    # Replace the old root with the new root in the tree
    tree._setroot(new_root)

    # Write the modified XML back to the file
    tree.write(xml_file)

# Example usage
if __name__ == "__main__":
    xml_file = 'router_backup.xml'  # Specify the path to the XML file
    new_root_tag = '{urn:ietf:params:xml:ns:netconf:base:1.0}config'  # Specify the new tag for the root element
    new_root_attributes = {}  # Specify the new attributes for the root element

    change_root(xml_file, new_root_tag, new_root_attributes)

    # Print the modified XML
    with open(xml_file, 'r') as f:
        modified_xml = f.read()
        print(modified_xml)
