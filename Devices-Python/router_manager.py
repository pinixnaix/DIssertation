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

    def get_interface_stats(self):
        try:
            with manager.connect(host=self.ip, port=self.port, username=self.username, password=self.password,
                                 hostkey_verify=False) as m:
                data = '''
                            <filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
                                <interfaces-state xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces"/>
                            </filter>
                        '''
                response = m.get(data)
                print("Router interface statistics retrieved successfully.")
            return response
        except Exception as e:
            print("Error:", e)

    def edit_interface(self, config):
        try:
            with manager.connect(host=self.ip, port=self.port, username=self.username, password=self.password,
                                 hostkey_verify=False) as m:

                response = m.edit_config(target="running", config=config)

            return response
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

    def write_to_influxdb(self, measurement, tag, data):
        try:
            client = influxdb_client.InfluxDBClient(url=self.influxdb_url,
                                                    token=self.influxdb_token,
                                                    org=self.influxdb_org)
            write_api = client.write_api(write_options=SYNCHRONOUS)
            for item in data:
                point = influxdb_client.Point(measurement)
                point.tag('host', self.ip)
                point.tag(tag, item["name"])
                for key, value in item["stats"].items():
                    point.field(key, value)
                write_api.write(bucket=self.influxdb_bucket, org=self.influxdb_org, record=point)
            print(f"Router data sent to InfluxDB successfully.")
            client.close()
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

    def get_interface_stats_from_influxdb(self, query):
        try:
            client = influxdb_client.InfluxDBClient(url=self.influxdb_url, token=self.influxdb_token)
            query_api = client.query_api()

            # Execute the Flux query received
            result = query_api.query(query, org=self.influxdb_org)

            print("Router interface stats retrieved from database successfully.")

            return result
        except Exception as e:
            print("Error:", e)
