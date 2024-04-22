from router_manager import Router
import time
from datetime import datetime, timedelta


# Function to build a query
def make_query(host, bucket, status, interface):
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(minutes=5)

    # Query for the router interface stats from InfluxDB
    query = f'''
              from(bucket: "{bucket}")
     |> range(start: {start_time.strftime('%Y-%m-%dT%H:%M:%SZ')}, stop: {end_time.strftime('%Y-%m-%dT%H:%M:%SZ')})
     |> filter(fn: (r) => r["_measurement"] == "interface_stats")
     |> filter(fn: (r) => r["host"] == "{host}")
     |> filter(fn: (r) => r["_field"] == "{status}")
     |> filter(fn: (r) => r["name"] == "{interface}")
     |> difference()
     |> filter(fn: (r) => r["_value"] != 0)
     |> count()
           '''
    return query


# Main function
def main():
    #
    router = Router("10.10.20.48", 830, "developer", "C1sco12345", "http://localhost:8086",
                    "B9ECClKQ2hbGsWnGH96M9a_wlMSzuRlrMBLBSmwiI3_85YkjP--0utdoIAE_fItt14sZK6j7dIBgj7tvo4RUMQ==",
                    "my-org", "network")

    # Builds and makes a Query for the interface admin status data from InfluxDB
    query = make_query("10.10.20.48", "network", "admin_status", "GigabitEthernet2")
    interface_data = router.get_interface_stats_from_influxdb(query)
    # if the query returns a list that is not empty prints
    # the total amount of times the admin status changed in the last 5 minutes,
    # else prints there is no changes
    if len(interface_data)>0:
        count = interface_data[0].records[0].get_value()
        print("Number of times interface admin status changed in the last 5 minutes:", count)
    else:
        print("No changes found in the interface admin status in the last 5 minutes")

    # Builds and makes a Query for the interface operational satus data from InfluxDB
    query = make_query("10.10.20.48", "network", "oper_status", "GigabitEthernet2")
    interface_data = router.get_interface_stats_from_influxdb(query)
    # if the query returns a list that is not empty prints
    # the total amount of times the admin status changed in the last 5 minutes,
    # else prints there is no changes
    if len(interface_data)>0:
        count = interface_data[0].records[0].get_value()
        print("Number of times interface operational status changed in the last 5 minutes:", count)
    else:
        print("No changes found in the interface operational status in the last 5 minutes")


# Execute the main function
if __name__ == "__main__":
    # runs the script every 5 minutes
    while True:
        main()
        time.sleep(300)
