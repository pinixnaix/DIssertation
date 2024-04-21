from ncclient import manager


def download_running_config(router_ip, username, password, output_file):
    try:
        # Connect to the router using NETCONF
        with manager.connect(host=router_ip,
                              port=830,
                              username=username,
                              password=password,
                              #device_params={'name': 'iosxe'},
                              hostkey_verify=False) as m:

            # Retrieve the running configuration
            running_config = m.get_config(source='running').data_xml
            print(running_config)
            print("Running configuration downloaded")
    except Exception as e:
        print("Error:", e)


def rollback_running_config(router_ip, username, password, output_file):
    try:
        with open(output_file, 'r') as file:
            running_config = file.read()
        # Connect to the router using NETCONF
        with manager.connect(host=router_ip,
                              port=830,
                              username=username,
                              password=password,
                              device_params={'name': 'iosxe'},
                              hostkey_verify=False) as m:

            # Rollback the running configuration
            m.edit_config(target='running', config=running_config, default_operation='replace')
            print("Running configuration rollback successfully:", output_file)

    except Exception as e:
        print("Error:", e)


# Example usage
if __name__ == "__main__":
    router_ip = '10.10.20.48'  # Replace 'router_ip' with the IP address of your router
    username = 'developer'  # Replace 'username' with your username
    password = 'C1sco12345'  # Replace 'password' with your password
    output_file = 'router_backup.xml'  # Specify the output file path

    #download_running_config(router_ip, username, password, output_file)
    rollback_running_config(router_ip, username, password, output_file)
