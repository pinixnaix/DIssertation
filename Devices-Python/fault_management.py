from router_manager import Router
import time
from datetime import datetime, timedelta


def make_query():
    query = f'''
                from(bucket: "network")
              |> range(start: -15s)
              |> filter(fn: (r) => r["_measurement"] == "interface_stats")
              |> pivot(rowKey:["name"], columnKey: ["_field"], valueColumn: "_value")
              |> group(columns: ["name"])
             '''

    return query


def interface_utilisation(router, data):
    result = []
    for table in data:
        for key in table.records:
            name = key['name']
            in_octets = key['in_octets']
            out_octets = key['out_octets']
            speed = key['speed']
            stat = ((in_octets + out_octets)/speed)*100
            result.append({'name': name,
                           'stats': {
                               'interface_utilisation': stat}})
    router.write_to_influxdb('fault_management_stats', 'name', result)


def traffic_volume(router, data):
    result = []
    for table in data:
        for key in table.records:
            name = key['name']
            in_octets = key['in_octets']
            out_octets = key['out_octets']
            stat = in_octets + out_octets
            result.append({'name': name,
                           'stats': {
                               'traffic_volume': stat}})
    router.write_to_influxdb('fault_management_stats', 'name', result)


def bit_error_rate(router, data):
    result = []
    for table in data:
        for key in table.records:
            name = key['name']
            in_errors = key['in_errors']
            out_octets = key['out_octets']
            if in_errors >= 0.0 and out_octets > 0.0:
                bir = (in_errors / out_octets) * 100.0
            else:
                bir = 0.0
            result.append({'name': name,
                           'stats': {
                               'bit_error_rate': bir}})
    router.write_to_influxdb('fault_management_stats', 'name', result)


def link_flap(router, data):
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(minutes=5)

    result = []
    for table in data:
        for key in table.records:
            name = key['name']
            query = f'''
                              from(bucket: "network")
                     |> range(start: {start_time.strftime('%Y-%m-%dT%H:%M:%SZ')}, stop: {end_time.strftime('%Y-%m-%dT%H:%M:%SZ')})
                     |> filter(fn: (r) => r["_measurement"] == "interface_stats")
                     |> filter(fn: (r) => r["host"] == "10.10.20.48")
                     |> filter(fn: (r) => r["_field"] == "admin_status")
                     |> filter(fn: (r) => r["name"] == "{name}")
                     |> difference()
                     |> filter(fn: (r) => r["_value"] != 0)
                     |> count()
                     '''
            stat = router.get_interface_stats_from_influxdb(query)
            if len(stat) == 0:
                stat = 0

            result.append({'name': name,
                           'stats': {
                               'link_stat': stat}})
    router.write_to_influxdb('fault_management_stats', 'name', result)


def calculate_bandwidth(stats):
    # Calculate difference in octets for inbound and outbound traffic
    in_octets_diff = int(stats[1][0]) - int(stats[0][0])
    out_octets_diff = int(stats[1][1]) - int(stats[0][1])

    # Calculate bandwidth utilization in bytes per second (Bps)
    in_bandwidth = in_octets_diff / 15
    out_bandwidth = out_octets_diff / 15

    return [round(in_bandwidth, 2), round(out_bandwidth, 2)]


def bandwidth(router, query, previous_data):
    previous_stats = []
    for table in previous_data:
        for key in table.records:
            in_octets = key['in_octets']
            out_octets = key['out_octets']
            previous_stats.append([in_octets, out_octets])
    time.sleep(15)
    current_data = router.get_interface_stats_from_influxdb(query)
    current_stats = []
    for table in current_data:
        for key in table.records:
            in_octets = key['in_octets']
            out_octets = key['out_octets']
            current_stats.append([in_octets, out_octets])
    results = []
    x = 0
    for table in previous_data:
        for key in table.records:
            band = calculate_bandwidth([previous_stats[x], current_stats[x]])
            name = key['name']
            interface_stats = {'name': name,
                               'stats': {
                                   'in_bandwidth': band[0],
                                   'out_bandwidth': band[1]}}
            results.append(interface_stats)
            x = x + 1

    router.write_to_influxdb('fault_management_stats', 'name', results)


def get_fault_management_statistics():
    try:
        router = Router("10.10.20.48", 830, "developer", "C1sco12345", "http://localhost:8086",
                        "my-super-secret-auth-token",
                        "my-org", "network")

        # Builds and makes a Query for the interface admin status data from InfluxDB
        query = make_query()
        interface_data = router.get_interface_stats_from_influxdb(query)
        #bit_error_rate(router, interface_data)
        #link_flap(router, interface_data)
        #bandwidth(router, query, interface_data)
        #traffic_volume(router, interface_data)
        interface_utilisation(router, interface_data)
    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    # Execute the function to retrieve interface statistics

    get_fault_management_statistics()
