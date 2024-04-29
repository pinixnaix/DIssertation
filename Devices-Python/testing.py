from router_manager import Router

try:
    router = Router("10.10.20.48", 830, "developer", "C1sco12345", "http://localhost:8086",
                    "my-super-secret-auth-token", "my-org", "network")

    router.run_to_startup()

except Exception as e:
    print("Error:", e)

