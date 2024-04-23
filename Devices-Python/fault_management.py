from router_manager import Router
import time


def make_query():
    query = f'''
                from(bucket: "network")
              |> range(start: -15s)
              |> filter(fn: (r) => r["_measurement"] == "interface_stats")
              |> pivot(rowKey:["name"], columnKey: ["_field"], valueColumn: "_value")
              |> group(columns: ["name"])
             '''

    return query


def build_fault_management_stats(stats):
   """ # Store interface statistics in a dictionary
    results = []

        interface_stats = {'name': name,
                           'stats': {
                               'bit_rate_error': ,
                               'bandwidth': ,
                               'speed': float(speed), 'in_errors': float(in_errors), 'in_octets': float(in_octets),
                               'traffic_volume': float(in_unicast_pkts), 'in_broadcast_pkts': float(in_broadcast_pkts),
                               'packets_discard': float(in_multicast_pkts), 'in_discards': float(in_discards),
                               'interface_speed': float(out_errors), 'out_octets': float(out_octets),
                               'interface_utilisation': float(out_unicast_pkts), 'out_broadcast_pkts': float(out_broadcast_pkts),
                               'link_flap': float(out_multicast_pkts), 'out_discards': float(out_discards)}}
        results.append(interface_stats)
        """


def bit_error_rate(data):
    result = []
    for table in data:
        for key in table.records:
            name = key['name']
            in_errors = key['in_errors']
            out_octets = key['out_octets']
            if in_errors >= 0.0 and out_octets > 0.0:
                bir = (in_errors/out_octets) * 100.0
            else:
                bir = 0.0
            result.append({name: bir})
    return result


def get_fault_management_statistics():
    try:
        router = Router("10.10.20.48", 830, "developer", "C1sco12345", "http://localhost:8086",
                        "my-super-secret-auth-token",
                        "my-org", "network")

        # Builds and makes a Query for the interface admin status data from InfluxDB
        query = make_query()
        interface_data = router.get_interface_stats_from_influxdb(query)
        print(bit_error_rate(interface_data))

    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    # Execute the function to retrieve interface statistics

   get_fault_management_statistics()

