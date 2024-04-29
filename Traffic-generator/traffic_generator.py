import random
import threading
import time
from scapy.all import IP, ICMP, TCP, UDP, send

def generate_icmp_traffic(destination_ips, interval=1):
    """
    Generate ICMP traffic to the specified destination IPs.
    """
    for destination_ip in destination_ips:
        packet_icmp = IP(dst=destination_ip) / ICMP()
        send(packet_icmp, verbose=False)
        time.sleep(interval)

def generate_tcp_traffic(destination_ips, interval=1, src_port=None, dst_port=None):
    """
    Generate TCP traffic to the specified destination IPs.
    """
    for destination_ip in destination_ips:
        payload_size = random.randint(1, 2000)  # Adjust payload size as needed
        payload = bytes([random.randint(0, 255) for _ in range(payload_size)])
        packet_tcp = IP(dst=destination_ip) / TCP(dport=dst_port, sport=src_port) / payload
        send(packet_tcp, verbose=False)
        time.sleep(interval)

def generate_udp_traffic(destination_ips, interval=1, src_port=None, dst_port=None):
    """
    Generate UDP traffic to the specified destination IPs.
    """
    for destination_ip in destination_ips:
        payload_size = random.randint(1, 2000)  # Adjust payload size as needed
        payload = bytes([random.randint(0, 255) for _ in range(payload_size)])
        packet_udp = IP(dst=destination_ip) / UDP(dport=dst_port, sport=src_port) / payload
        send(packet_udp, verbose=False)
        time.sleep(interval)

def stress_test(destination_ips, duration, discard_prob=0.1, lost_prob=0.1):
    """
    Stress test the target IPs by generating continuous traffic for the specified duration.
    """
    print("Stress test started.")
    end_time = time.time() + duration
    while time.time() < end_time:
        for destination_ip in destination_ips:
            # Randomly discard packets
            if random.random() < discard_prob:
                continue

            # Generate ICMP packet
            packet_icmp = IP(dst=destination_ip) / ICMP()

            # Randomly lose packets
            if random.random() < lost_prob:
                continue

            send(packet_icmp, verbose=False)

    print("Stress test completed.")

def run(destination_ips, duration, discard_prob=0.1, lost_prob=0.1):
    """
    Main function to run traffic generation and stress test.
    """
    # Set the interval between packets in seconds
    packet_interval = 1

    # Create a thread for the stress test
    stress_thread = threading.Thread(target=stress_test, args=(destination_ips, duration, discard_prob, lost_prob))
    stress_thread.start()

    try:
        while True:
            # Generate ICMP traffic
            generate_icmp_traffic(destination_ips, packet_interval)
            print("Sent ICMP packet")

            # Generate TCP traffic
            generate_tcp_traffic(destination_ips, packet_interval, src_port=1234, dst_port=80)
            print("Sent TCP packet")

            # Generate UDP traffic
            generate_udp_traffic(destination_ips, packet_interval, src_port=5678, dst_port=53)
            print("Sent UDP packet")

    except KeyboardInterrupt:
        print("Traffic generation stopped.")
        stress_thread.join()  # Wait for stress test thread to finish

if __name__ == "__main__":
    destination_ips = ["10.10.20.48", "10.10.10.38", "10.10.30.38"]  # List of destination IPs
    duration = 60  # Duration of the stress test in seconds
    discard_prob = 0.1  # Probability of discarding packets (10%)
    lost_prob = 0.1  # Probability of losing packets (10%)

    run(destination_ips, duration, discard_prob, lost_prob)
