# Import API libraries
from ncclient import manager
import xmltodict


def display(data):
    for process in data:
        print("""PID: {}\nNAME: {}\nTTY: {}\nTOTAL RUN TIME: {}\nINVOCATION COUNT: {}\nAVG RUN TIME: {}
FIVE SECONDS: {}\nONE MINUTE: {}\nFIVE MINUTES: {}\n""".format(
            process["pid"], process["name"], process["tty"], process["total-run-time"],
            process["invocation-count"], process["avg-run-time"], process["five-seconds"],
            process["one-minute"], process["five-minutes"]))


def run():
    with manager.connect(
            host="10.10.20.48",
            port=830,
            username="developer",
            password="C1sco12345",
            hostkey_verify=False
    ) as m:
        cpu_usage = """
         <filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
                <cpu-usage xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-process-cpu-oper"/>
         </filter>

        """

        netconf_reply = m.get(filter=cpu_usage).xml

        cpu = xmltodict.parse(netconf_reply)["rpc-reply"]["data"]["cpu-usage"]["cpu-utilization"]\
            ["cpu-usage-processes"]["cpu-usage-process"]

        display(cpu)


if __name__ == "__main__":
    run()
