import random
import time
from router_manager import Router


def build_config(interface, enabled):
    config = f"""
             <config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
                 <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
                    <interface>
                        <name>{interface}</name>
                        <enabled>{enabled}</enabled>
                    </interface>
                 </interfaces>
             </config>
            """
    return config


def randomly_change_interface_state(router):
    interfaces = ["GigabitEthernet2", "GigabitEthernet3"]
    enabled_states = ["true", "false"]
    interface = random.choice(interfaces)
    enabled = random.choice(enabled_states)
    config = build_config(interface, enabled)
    response = router.edit_router(config)
    if response.ok:
        print(f"Router interface {interface} changed to enabled={enabled} successfully!!")
    else:
        print(f"Failed to change router interface {interface} to enabled={enabled}!!")


def run():
    try:
        router = Router("10.10.20.48", 830, "developer", "C1sco12345", "http://localhost:8086",
                        "8HYXrEbdGmbFYXy6KILdvVrmZfEl6X_CoU_qUDW6nx-QeWMgK9R-jm2Q_fxj3Jx9IwL1NPTp5tDnmE1P3dhRkg==",
                        "my-org", "network")

        while True:
            randomly_change_interface_state(router)
            time.sleep(random.randint(1, 10))  # Sleep for random duration between 1 to 10 seconds before next change

    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    run()
