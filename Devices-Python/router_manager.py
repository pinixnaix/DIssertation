import xmltodict
from ncclient import manager
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS


class Router:
    def __init__(self, ip, port, username, password, url, token, org, bucket):
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password
        self.influxdb_url = url
        self.influxdb_token = token
        self.influxdb_org = org
        self.influxdb_bucket = bucket

    def backup_configuration(self):
        try:
            with manager.connect(host=self.ip, port=self.port, username=self.username, password=self.password,
                                 hostkey_verify=False) as m:
                configuration = m.get_config(source='running').data_xml
                print("Router configuration retrieved successfully.")
            return configuration
        except Exception as e:
            print("Error:", e)

    def rollback_configuration(self, config):
        try:
            with manager.connect(host=self.ip, port=self.port, username=self.username, password=self.password,
                                 hostkey_verify=False) as m:
                m.edit_config(target='running', config=config)
                print("Router configuration rollback completed successfully.")
        except Exception as e:
            print("Error:", e)

    def write_to_influxdb(self, config):
        try:
            client = influxdb_client.InfluxDBClient(url=self.influxdb_url, token=self.influxdb_token, org=self.influxdb_org)
            write_api = client.write_api(write_options=SYNCHRONOUS)
            point = influxdb_client.Point("router_config").tag("host", self.ip).field("config", config)
            write_api.write(bucket=self.influxdb_bucket, org=self.influxdb_org, record=point)
            print("Router configuration backup sent to InfluxDB successfully.")
        except Exception as e:
            print("Error:", e)

    def get_config_from_influxdb(self):
        try:
            client = influxdb_client.InfluxDBClient(url=self.influxdb_url, token=self.influxdb_token)
            query_api = client.query_api()

            # Query the most recent router configuration from InfluxDB
            query = f'from(bucket: "{self.influxdb_bucket}") |> range(start: -1h) |> ' \
                    f'filter(fn: (r) => r["host"] == "10.10.20.48") |> last()'
            # Execute the Flux query
            tables = query_api.query(query, org=self.influxdb_org)

            # Extract configuration data from the query result
            for table in tables:
                for row in table.records:
                    configuration = row['_value']

            print("Router configuration retrieved from database successfully.")
            return configuration
        except Exception as e:
            print("Error:", e)

    def get_interface_stats_from_influxdb(self):
        try:
            client = influxdb_client.InfluxDBClient(url=self.influxdb_url, token=self.influxdb_token)
            query_api = client.query_api()

            # Query the most recent router configuration from InfluxDB
            query = f'''
                    from(bucket: "{self.influxdb_bucket}")
                      |> range(start: -5m)  # Retrieve data for the last 5 minutes
                      |> filter(fn: (r) => r["_measurement"] == "interface_status")  # Filter by measurement name
                      |> filter(fn: (r) => r["interface_name"] == "GigabitEthernet1")  # Filter by interface name
                      |> filter(fn: (r) => r["_field"] == "admin_status" or r["_field"] == "oper_status")  # Filter by field name
                      |> last()  # Retrieve the last value within the specified range
                '''
            # Execute the Flux query
            result = query_api.query(query, org=self.influxdb_org)

            print("Router interface stats retrieved from database successfully.")

            return result
        except Exception as e:
            print("Error:", e)