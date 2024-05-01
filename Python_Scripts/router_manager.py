from ncclient import manager, xml_  # Importing ncclient modules for NETCONF operations
import influxdb_client  # Importing InfluxDB client library
from influxdb_client.client.write_api import SYNCHRONOUS  # Importing write API for InfluxDB


class Router:
    def __init__(self, ip, port, username, password, url, token, org, bucket):
        """
        Initialize Router object with connection parameters.

        Args:
            ip (str): IP address of the router.
            port (int): Port number for connection.
            username (str): Username for authentication.
            password (str): Password for authentication.
            url (str): URL for InfluxDB connection.
            token (str): Authentication token for InfluxDB.
            org (str): Organization name for InfluxDB.
            bucket (str): Bucket name for InfluxDB.
        """
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password
        self.influxdb_url = url
        self.influxdb_token = token
        self.influxdb_org = org
        self.influxdb_bucket = bucket

    def run_to_startup(self):
        """
        Save the running configuration to the startup configuration on the router.
        """
        try:
            with manager.connect(host=self.ip, port=self.port, username=self.username, password=self.password,
                                 hostkey_verify=False) as m:
                save = """
                <cisco-ia:save-config xmlns:cisco-ia="http://cisco.com/yang/cisco-ia"/>
                """
                reply = m.dispatch(xml_.to_ele(save))
                if reply.ok:
                    print("Running configuration saved to startup configuration successfully.")
                else:
                    print("Failed to save running configuration to startup configuration.")
        except Exception as e:
            print("Error:", e)

    def backup_configuration(self):
        """
        Backup the running configuration from the router.
        """
        try:
            with manager.connect(host=self.ip, port=self.port, username=self.username, password=self.password,
                                 hostkey_verify=False) as m:
                configuration = m.get_config(source='running').data_xml
                print("Router running configuration retrieved successfully.")
            return configuration
        except Exception as e:
            print("Error:", e)

    def get_stats(self, data):
        """
        Retrieve statistics from the router.

        Args:
            data (str): XML filter for retrieving specific statistics.

        Returns:
            Response: Statistics response from the router.
        """
        try:
            with manager.connect(host=self.ip, port=self.port, username=self.username, password=self.password,
                                 hostkey_verify=False) as m:
                response = m.get(data)
                print("Router statistics retrieved successfully.")
            return response
        except Exception as e:
            print("Error:", e)

    def edit_router(self, config):
        """
        Edit router configuration.

        Args:
            config (str): XML configuration string to edit router configuration.

        Returns:
            Response: Response from the router after editing configuration.
        """
        try:
            with manager.connect(host=self.ip, port=self.port, username=self.username, password=self.password,
                                 hostkey_verify=False) as m:
                response = m.edit_config(target="running", config=config)
                print("Router modifications done successfully.")
            return response
        except Exception as e:
            print("Error:", e)

    def rollback_configuration(self, config):
        """
        Rollback router configuration to a previous state.

        Args:
            config (str): XML configuration string for rollback.
        """
        try:
            with manager.connect(host=self.ip, port=self.port, username=self.username, password=self.password,
                                 hostkey_verify=False) as m:
                m.edit_config(target='running', config=config)
                print("Router configuration rollback completed successfully.")
        except Exception as e:
            print("Error:", e)

    def write_to_influxdb(self, measurement, tag, data):
        """
        Write data to InfluxDB.

        Args:
            measurement (str): Name of the measurement.
            tag (str): Tag name.
            data (list): Data to be written to InfluxDB.
        """
        try:
            client = influxdb_client.InfluxDBClient(url=self.influxdb_url,
                                                    token=self.influxdb_token,
                                                    org=self.influxdb_org)
            write_api = client.write_api(write_options=SYNCHRONOUS)
            if measurement == "router_config":
                point = influxdb_client.Point(measurement)
                point.tag('host', self.ip)
                point.field(tag, data)
                write_api.write(bucket=self.influxdb_bucket, org=self.influxdb_org, record=point)
            else:
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
        """
        Retrieve router configuration from InfluxDB.

        Returns:
            str: Router configuration retrieved from database.
        """
        try:
            client = influxdb_client.InfluxDBClient(url=self.influxdb_url, token=self.influxdb_token)
            query_api = client.query_api()

            # Query the most recent router configuration from InfluxDB
            query = f"""
                        from(bucket: "network")
              |> range(start: -1h)
              |> filter(fn: (r) => r["_measurement"] == "router_config")
              |> filter(fn: (r) => r["host"] == "{self.ip}")
              |> filter(fn: (r) => r["_field"] == "running-config")
              |> yield(name: "last")
            """
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
        """
        Retrieve router interface statistics from InfluxDB.

        Args:
            query (str): Flux query to retrieve interface statistics.

        Returns:
            result: Router interface statistics retrieved from database.
        """
        try:
            client = influxdb_client.InfluxDBClient(url=self.influxdb_url, token=self.influxdb_token)
            query_api = client.query_api()

            # Execute the Flux query received
            result = query_api.query(query, org=self.influxdb_org)

            print("Router interface stats retrieved from database successfully.")

            return result
        except Exception as e:
            print("Error:", e)
