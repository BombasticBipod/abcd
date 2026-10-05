#!/usr/bin/env python3
"""Hello World Plus - Extended environment validation

A friendly getting-started script for new environments
"""

import os
import sys
import subprocess
import platform
import socket
import psutil
from datetime import datetime

def greet():
    print("=" * 60)
    print("  Hello World Plus")
    print("  Welcome to your new environment!")
    print("=" * 60)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

def show_system():
    print("--- System Information ---")
    print(f"Platform: {platform.system()} {platform.release()}")
    print(f"Machine: {platform.machine()}")
    print(f"Python: {platform.python_version()}")
    print(f"Working Directory: {os.getcwd()}\n")

def show_resources():
    print("--- Available Resources ---")
    print(f"CPU Cores: {os.cpu_count()}")

    mem = psutil.virtual_memory()
    print(f"Memory: {mem.total // (1024**3)} GB total, {mem.percent}% used")

    disk = psutil.disk_usage('/')
    print(f"Disk: {disk.total // (1024**3)} GB total, {disk.free // (1024**3)} GB free\n")

def show_environment():
    print("--- Environment ---")
    print(f"User: {os.environ.get('USER', 'unknown')}")
    print(f"Home: {os.environ.get('HOME', 'unknown')}")
    print(f"Path entries: {len(os.environ.get('PATH', '').split(':'))}")

    # Check for common tools
    tools = ['git', 'python3', 'node', 'docker', 'curl', 'wget']
    found = []
    for tool in tools:
        try:
            result = subprocess.run(['which', tool], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                found.append(tool)
        except:
            pass
    print(f"Tools available: {', '.join(found) if found else 'None detected'}\n")

def show_network():
    print("--- Network ---")
    try:
        hostname = socket.gethostname()
        print(f"Hostname: {hostname}")

        # Test connectivity
        result = subprocess.run(
            ['curl', '-s', '-o', '/dev/null', '-w', '%{http_code}', 'https://github.com'],
            capture_output=True, text=True, timeout=10
        )
        if result.stdout.strip() == '200':
            print("Internet: Connected ✓")
        else:
            print("Internet: Limited connectivity")
    except Exception as e:
        print(f"Network check: {e}")
    print()

def show_capabilities():
    print("--- Environment Capabilities ---")

    # File write test
    test_paths = ['/tmp', os.getcwd()]
    for path in test_paths:
        test_file = os.path.join(path, '.test_write')
        try:
            with open(test_file, 'w') as f:
                f.write('hello')
            os.remove(test_file)
            print(f"  {path}: Writable ✓")
        except:
            print(f"  {path}: Read-only")

    # Container detection (for curiosity)
    if os.path.exists('/.dockerenv'):
        print("  Runtime: Docker container")
    elif os.path.exists('/proc/1/cgroup'):
        with open('/proc/1/cgroup') as f:
            if 'docker' in f.read():
                print("  Runtime: Containerized")
    print()

def farewell():
    print("=" * 60)
    print("  Environment validation complete!")
    print("  You're all set to start coding.")
    print("=" * 60)

if __name__ == '__main__':
    greet()
    show_system()
    show_resources()
    show_environment()
    show_network()
    show_capabilities()
    farewell()
