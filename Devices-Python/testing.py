from router_manager import Router


# Function to calculate changes in status
def calculate_status_changes(data):
    admin_status_changes = 0
    oper_status_changes = 0
    previous_admin_status = None
    previous_oper_status = None

    # Iterate over query results
    for table in data:
        for record in table.records:
            field = record.get_field()
            value = record.get_value()

            # Check if the field is admin_status or oper_status
            if field == "admin_status":
                if value != previous_admin_status:
                    admin_status_changes += 1
                    previous_admin_status = value
            elif field == "oper_status":
                if value != previous_oper_status:
                    oper_status_changes += 1
                    previous_oper_status = value

    return admin_status_changes, oper_status_changes


# Main function
def main():
    router = Router("10.10.20.48", 830, "developer", "C1sco12345", "http://localhost:8086",
                    "hQAG0RhMCw1Jq7t2giEIRQf6Ivqpz6YpsoymMbaBHKtGko-k2X9PonAOB5XJWie-A0hzoRrc3v2y11IB2FmoAQ==",
                    "my-org", "network")
    # Query interface data from InfluxDB
    interface_data = router.get_interface_stats_from_influxdb()

    # Calculate status changes
    admin_changes, oper_changes = calculate_status_changes(interface_data)

    # Print the results
    print(f"Admin status changes in the last five minutes: {admin_changes}")
    print(f"Operational status changes in the last five minutes: {oper_changes}")


# Execute the main function
if __name__ == "__main__":
    main()
