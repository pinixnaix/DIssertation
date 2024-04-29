from router_manager import Router
import time
from datetime import datetime, timedelta

interval = 30


def make_query():
    query = f'''
                from(bucket: "network")
              |> range(start: -15s)
              |> filter(fn: (r) => r["_measurement"] == "interface_stats")
              |> pivot(rowKey:["name"], columnKey: ["_field"], valueColumn: "_value")
              |> group(columns: ["name"])
             '''

    return query


def traffic(router, new_data, old_data):
    previous, result, recent, counter = [], [], [], 0
    for table in old_data:
        for key in table.records:
            in_octets = key['in_octets']
            out_octets = key['out_octets']
            total = in_octets + out_octets
            previous.append([in_octets, out_octets, total])
    for table in new_data:
        for key in table.records:
            in_octets = key['in_octets']
            out_octets = key['out_octets']
            total = in_octets + out_octets
            recent.append([in_octets, out_octets, total])
    for table in old_data:
        for key in table.records:
            name = key['name']
            speed = key['speed']
            stat = calculate_traffic([previous[counter], recent[counter]], speed)
            result.append({'name': name,
                           'stats': {
                               'in_traffic': stat[0],
                               'out_traffic': stat[1],
                               'traffic_volume': stat[2],
                               'in_utilisation': stat[3],
                               'out_utilisation': stat[4]}})
            counter = counter + 1

    router.write_to_influxdb('fault_management_stats', 'name', result)


def rate(router, data):
    result = []

    for table in data:
        for key in table.records:
            total, total_errors, total_discards = 0, 0, 0
            name = key['name']
            total_errors += key['in_errors']
            total_errors += key['out_errors']
            total_discards += key['in_discards']
            total_discards += key['out_discards']
            total += key['in_unicast_pkts']
            total += key['out_unicast_pkts']
            total += key['in_multicast_pkts']
            total += key['out_multicast_pkts']
            total += key['in_broadcast_pkts']
            total += key['out_broadcast_pkts']

            if total == 0:
                error_rate = 0
                discard_rate = 0
            else:
                error_rate = (int(total_errors) / int(total)) * 100
                discard_rate = (int(total_discards) / int(total)) * 100
            result.append({'name': name,
                           'stats': {
                               'error_rate': float(error_rate),
                               'discard_rate': float(discard_rate)}})
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
                counter = 0
            else:
                for record in stat:
                    counter = record.records[0]['_value']

            result.append({'name': name,
                           'stats': {
                               'link_flap': counter}})
    router.write_to_influxdb('fault_management_stats', 'name', result)


def calculate_traffic(stats, speed):
    # Calculate difference in octets for inbound, outbound and total traffic
    in_octets_diff = int(stats[1][0]) - int(stats[0][0])
    out_octets_diff = int(stats[1][1]) - int(stats[0][1])
    total = int(stats[1][2]) - int(stats[0][2])

    # Calculate interface traffic and utilisation in a 30s interval in Bytes per second (Bps)
    in_traffic = in_octets_diff / interval
    out_traffic = out_octets_diff / interval
    total_traffic = total / interval
    in_utilisation = (in_octets_diff / (interval * speed)) * 100
    out_utilisation = (out_octets_diff / (interval * speed)) * 100

    return [in_traffic, out_traffic, total_traffic, in_utilisation, out_utilisation]


def get_fault_management_statistics():
    try:
        router = Router("10.10.20.48", 830, "developer", "C1sco12345", "http://localhost:8086",
                        "my-super-secret-auth-token",
                        "my-org", "network")

        # Builds and makes a Query for the interface admin status data from InfluxDB
        old_query = make_query()
        old_data = router.get_interface_stats_from_influxdb(old_query)
        time.sleep(interval)
        new_query = make_query()
        new_data = router.get_interface_stats_from_influxdb(new_query)

        rate(router, new_data)
        link_flap(router, new_data)
        traffic(router, new_data, old_data)

    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    # Execute the function to retrieve interface statistics
    while True:
        get_fault_management_statistics()
        time.sleep(30)
