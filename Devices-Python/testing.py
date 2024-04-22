from router_manager import Router
import time

interval = 15


# Function to build a query
def make_query(host, bucket, interface):
    # Query for the router interface stats from InfluxDB
    query = f'''
              last_in_octets = from(bucket: "{bucket}")
      |> range(start: -10s)
      |> filter(fn: (r) => r["_measurement"] == "interface_stats")
      |> filter(fn: (r) => r["host"] == "{host}")
      |> filter(fn: (r) => r["name"] == "{interface}")
      |> filter(fn: (r) => r["_field"] == "in_octets" or r["_field"] == "out_octets")
      |> yield(name: "last")
          '''
    return query


def calculate_bandwidth(stats):
    # Calculate difference in octets for inbound and outbound traffic
    in_octets_diff = int(stats[1][0]) - int(stats[0][0])
    out_octets_diff = int(stats[1][1]) - int(stats[0][1])

    # Calculate bandwidth utilization in bytes per second (Bps)
    in_bandwidth = in_octets_diff / interval
    out_bandwidth = out_octets_diff / interval

    return [round(in_bandwidth, 2), round(out_bandwidth, 2)]


# Main function
def main():
    #
    stats = []
    router = Router("10.10.20.48", 830, "developer", "C1sco12345", "http://localhost:8086",
                    "B9ECClKQ2hbGsWnGH96M9a_wlMSzuRlrMBLBSmwiI3_85YkjP--0utdoIAE_fItt14sZK6j7dIBgj7tvo4RUMQ==",
                    "my-org", "network")

    # Builds and makes a Query for the interface stats data from InfluxDB
    query = make_query("10.10.20.48", "network", "GigabitEthernet1")
    interface_data = router.get_interface_stats_from_influxdb(query)
    previous_stats = [interface_data[0].records[0].get_value(), interface_data[1].records[0].get_value()]
    stats.append(previous_stats)
    time.sleep(interval)
    interface_data = router.get_interface_stats_from_influxdb(query)
    current_stats = [interface_data[0].records[0].get_value(), interface_data[1].records[0].get_value()]
    stats.append(current_stats)
    result = calculate_bandwidth(stats)
    print(f"Interface: GigabitEthernet1, In Bandwidth: {result[0]} Bps, Out Bandwidth: {result[1]} Bps")


# Execute the main function
if __name__ == "__main__":

    main()

