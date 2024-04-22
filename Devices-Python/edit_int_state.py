from router_manager import Router


def build_config(interface, enabled):
    config = f"""
             <config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
                 <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
                    <interface>
                        <name>{interface}</name>
                        <enabled>{enabled}</enabled>
                    </interface>
                 </interfaces >
             </config>
            """
    return config


def run():
    try:
        router = Router("10.10.20.48", 830, "developer", "C1sco12345", "http://localhost:8086",
                        "B9ECClKQ2hbGsWnGH96M9a_wlMSzuRlrMBLBSmwiI3_85YkjP--0utdoIAE_fItt14sZK6j7dIBgj7tvo4RUMQ==",
                        "my-org", "network")

        config = build_config("GigabitEthernet2", "true")
        # Send NETCONF <get> operation with the filter
        response = router.edit_interface(config)
        if response.ok is True:
            print("Router interface changed successfully!!")
        else:
            print("Router interface change not successfully!!")

    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    run()
