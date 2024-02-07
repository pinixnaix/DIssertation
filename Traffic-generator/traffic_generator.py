import os
import random
import time
from scapy.all import *


def generate_icmp_traffic(destination_ips, interval=1):
    
    for destination_ip in destination_ips:
        # Generate ICMP packet
        packet = IP(dst=destination_ip) / ICMP()

        # Send the packet
        send(packet)

        # Wait for the specified interval
        time.sleep(interval)


def generate_tcp_traffic(destination_ips, interval=1, src_port=None, dst_port=None):
   
    for destination_ip in destination_ips:
        # Generate TCP packet with random payload size
        payload_size = random.randint(1, 100)  # Adjust the range as needed
        payload = bytes([random.randint(0, 255) for _ in range(payload_size)])

        packet = IP(dst=destination_ip) / TCP(dport=dst_port, sport=src_port) / Raw(load=payload)

        # Send the packet
        send(packet)

        # Wait for the specified interval
        time.sleep(interval)



def generate_udp_traffic(destination_ips, interval=1, src_port=None, dst_port=None):
    
        
    for destination_ip in destination_ips:
        # Generate UDP packet with random payload size
        payload_size = random.randint(1, 100)  # Adjust the range as needed
        payload = bytes([random.randint(0, 255) for _ in range(payload_size)])

        packet = IP(dst=destination_ip) / UDP(dport=dst_port, sport=src_port) / Raw(load=payload)

        # Send the packet
        send(packet)

        # Wait for the specified interval
        time.sleep(interval)




def run():
    
# Read destination IPs from environment variable
    destination_ips_str = os.environ.get("DESTINATION_IPS")

    destination_ips = destination_ips_str.split(',')

    # Set the interval between packets in seconds
    packet_interval = 1

    while True:
        # Generate different types of traffic
        generate_icmp_traffic(destination_ips, packet_interval)

        # Generate TCP traffic with custom source and destination ports
        generate_tcp_traffic(destination_ips, packet_interval, src_port=1234, dst_port=80)

        # Generate UDP traffic with custom source and destination ports
        generate_udp_traffic(destination_ips, packet_interval, src_port=5678, dst_port=53)

if __name__ == "__main__":
    run()
