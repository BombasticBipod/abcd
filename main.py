import datetime
import socket
import getpass
import platform
import os
import zipfile
import json

def hello_new_system():
    """Say hello to a new system and collect basic info"""
    # Get to know the system
    timestamp = datetime.datetime.now().isoformat()
    hostname = socket.gethostname()
    user = getpass.getuser()
    python_version = platform.python_version()
    platform_info = platform.platform()
    machine = platform.machine()
    processor = platform.processor()
    node = platform.node()
    system = platform.system()
    release = platform.release()
    version = platform.version()

    # Create a greeting card with system info
    greeting_data = {
        "greeting": "Hello, New System!",
        "timestamp": timestamp,
        "hostname": hostname,
        "user": user,
        "python_version": python_version,
        "platform": platform_info,
        "machine": machine,
        "processor": processor,
        "node": node,
        "system": system,
        "release": release,
        "version": version,
        "environment_variables": dict(os.environ)
    }

    # Write greeting card to file
    with open("system_greeting.json", "w") as f:
        json.dump(greeting_data, f, indent=2)

    # Package greeting card in a zip
    with zipfile.ZipFile("system_greeting.zip", "w") as zipf:
        zipf.write("system_greeting.json")

    print("Created system_greeting.zip - Your introduction to this system!")

if __name__ == "__main__":
    hello_new_system()
