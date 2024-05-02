# Network Management and Monitoring System using NETCONF

## Overview
This repository contains a network management and monitoring system developed using the NETCONF protocol. The system was developed for a Dissertaion and aims to provide efficient data collection, configuration management, and fault detection capabilities within network environments.

## Requirements
- NETCONF protocol knowledge
- Docker installed on your machine
- Python installed on your machine
- Cisco DevNet Sandbox account (https://developer.cisco.com/)
- Access to reserve a Cisco DevNet Sandbox IOS XE on a Catalyst 8000V Edge Software-Defined WAN (SD-WAN) router
- VPN client (OpenConnect-GUI recommended)

## Setup Instructions
1. Clone this repository to your local machine:

          git clone https://github.com/pinixnaix/DIssertation.git

2. Navigate to the project directory:

3. Ensure Docker is running on your machine.

4. Reserve a Cisco DevNet Sandbox IOS XE on a Catalyst 8000V Edge SD-WAN router using your Cisco DevNet Sandbox account. Follow the instructions provided by Cisco for reservation.

5. Connect to the Cisco DevNet Sandbox VPN using the OpenConnect-GUI VPN client or any compatible VPN client. This step is necessary to access the reserved sandbox environment.

6. Once the sandbox is reserved and accessible, update the necessary files with the appropriate credentials and IP address of the sandbox router.

7. Update the credentials for the Docker containers (InfluxDB and Grafana) if necessary by modifying the `configuration.env` file and also the Python Scripts.

8. Update the Grafana contact points for the notification for another of your choice.  

9. Run the Python scripts to start the system:
   - `get_interfaces_state.py`: This script retrieves the state of network interfaces.
   - `get_cpu_usage_processes.py`: This script collects CPU usage and running processes data.
   - `fault_management.py`: This script handles fault management, including proactive fault detection.
   - `get_memory_stats.py`: This script gathers memory statistics from the network devices.

   To run a script, use the following command:

          python get_interfaces_state.py

10. The system should start collecting data, managing configurations, and detecting faults using the NETCONF protocol.

## Usage
- Once the system is running, To visualize the data collected by these scripts, access Grafana using the following link:
  [Grafana Dashboard](http://localhost:3000)
- Make any necessary adjustments to the configuration or implementation based on your specific network environment and requirements.



