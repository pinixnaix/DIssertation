import random  # Importing random module for generating random numbers
import time  # Importing time module for time-related operations
# Import necessary classes and functions from the scapy module for creating and sending packets
from scapy.all import IP, ICMP, TCP, UDP, send


def generate_icmp_traffic(destination_ips, interval=1):
    """
    Generate ICMP traffic to the specified destination IPs.

    Args:
        destination_ips (list): List of destination IP addresses.
        interval (float, optional): Time interval between packets. Defaults to 1 second.
    """
    for destination_ip in destination_ips:
        # Create ICMP packet
        packet_icmp = IP(dst=destination_ip) / ICMP()
        # Send ICMP packet
        send(packet_icmp, verbose=False)
        # Wait for the specified interval before sending the next packet
        time.sleep(interval)


def generate_tcp_traffic(destination_ips, interval=1, src_port=None, dst_port=None):
    """
    Generate TCP traffic to the specified destination IPs.

    Args:
        destination_ips (list): List of destination IP addresses.
        interval (float, optional): Time interval between packets. Defaults to 1 second.
        src_port (int, optional): Source port number. Defaults to None.
        dst_port (int, optional): Destination port number. Defaults to None.
    """
    for destination_ip in destination_ips:
        # Generate random payload size
        payload_size = random.randint(1000, 3000)
        # Generate payload data
        payload = bytes([random.randint(0, 255) for _ in range(payload_size)])
        # Create TCP packet
        packet_tcp = IP(dst=destination_ip) / TCP(dport=dst_port, sport=src_port) / payload
        # Send TCP packet
        send(packet_tcp, verbose=False)
        # Wait for the specified interval before sending the next packet
        time.sleep(interval)


def generate_udp_traffic(destination_ips, interval=1, src_port=None, dst_port=None):
    """
    Generate UDP traffic to the specified destination IPs.

    Args:
        destination_ips (list): List of destination IP addresses.
        interval (float, optional): Time interval between packets. Defaults to 1 second.
        src_port (int, optional): Source port number. Defaults to None.
        dst_port (int, optional): Destination port number. Defaults to None.
    """
    for destination_ip in destination_ips:
        # Generate random payload size
        payload_size = random.randint(1000, 3000)
        # Generate payload data
        payload = bytes([random.randint(0, 255) for _ in range(payload_size)])
        # Create UDP packet
        packet_udp = IP(dst=destination_ip) / UDP(dport=dst_port, sport=src_port) / payload
        # Send UDP packet
        send(packet_udp, verbose=False)
        # Wait for the specified interval before sending the next packet
        time.sleep(interval)


def run_traffic(destination_ips, duration):
    """
    Run traffic generation for the specified duration.

    Args:
        destination_ips (list): List of destination IP addresses.
        duration (int): Duration of the traffic generation in seconds.
    """
    print("Traffic generation started.")
    # Calculate the end time for traffic generation
    end_time = time.time() + duration
    # Continue generating traffic until the end time is reached
    while time.time() < end_time:
        # Generate ICMP traffic
        generate_icmp_traffic(destination_ips)
        print("Sent ICMP packet")

        # Generate TCP traffic
        generate_tcp_traffic(destination_ips, src_port=1234, dst_port=80)
        print("Sent TCP packet")

        # Generate UDP traffic
        generate_udp_traffic(destination_ips, src_port=5678, dst_port=53)
        print("Sent UDP packet")

    print("Traffic generation completed.")


if __name__ == "__main__":
    # List of destination IP addresses
    destination_ips = ["10.10.20.48", "10.10.10.38", "10.10.30.38"]
    # Duration of the traffic generation in seconds
    duration = 300

    # Run traffic generation
    run_traffic(destination_ips, duration)
