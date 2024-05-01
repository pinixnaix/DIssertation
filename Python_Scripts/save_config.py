from router_manager import Router  # Importing Router class from router_manager module

try:
    # Creating an instance of Router with connection parameters
    router = Router("10.10.20.48", 830, "developer", "C1sco12345", "http://localhost:8086",
                    "my-super-secret-auth-token", "my-org", "network")

    # Running the router's 'run_to_startup' method
    router.run_to_startup()

except Exception as e:
    # Handling exceptions by printing the error message
    print("Error:", e)
