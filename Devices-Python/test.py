import xmltodict

from router_manager import Router


def run():
    router = Router("10.10.20.48", 830, "developer", "C1sco12345", "http://localhost:8086",
                    "hQAG0RhMCw1Jq7t2giEIRQf6Ivqpz6YpsoymMbaBHKtGko-k2X9PonAOB5XJWie-A0hzoRrc3v2y11IB2FmoAQ==",
                    "my-org", "network")

    config = router.backup_configuration()
    router.write_to_influxdb(config)
    #backup_config = router.get_from_influxdb()
    #router.rollback_configuration(backup_config)


if __name__ == "__main__":
    run()
