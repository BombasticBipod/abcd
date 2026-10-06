#!/usr/bin/env python3
"""
system_audit.py - Comprehensive system information gatherer
Run this on your remote Linux system to collect all available info
"""

import os
import sys
import subprocess
import json
import datetime
import platform
import socket
import getpass

def run_cmd(cmd, timeout=30):
    """Run a shell command and return output"""
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, timeout=timeout
        )
        return result.stdout + result.stderr if result.stderr else result.stdout
    except Exception as e:
        return f"ERROR: {str(e)}"

def gather_system_info():
    """Collect comprehensive system information"""
    timestamp = datetime.datetime.now().isoformat()
    hostname = socket.gethostname()
    user = getpass.getuser()

    report = []
    report.append("=" * 80)
    report.append(f"COMPREHENSIVE SYSTEM AUDIT")
    report.append(f"Generated: {timestamp}")
    report.append(f"Hostname: {hostname}")
    report.append(f"User: {user}")
    report.append("=" * 80)
    report.append("")

    # Basic Python/Platform Info
    report.append("-" * 40)
    report.append("PYTHON & PLATFORM INFO")
    report.append("-" * 40)
    report.append(f"Python version: {platform.python_version()}")
    report.append(f"Platform: {platform.platform()}")
    report.append(f"Machine: {platform.machine()}")
    report.append(f"Processor: {platform.processor()}")
    report.append(f"Node: {platform.node()}")
    report.append(f"System: {platform.system()}")
    report.append(f"Release: {platform.release()}")
    report.append(f"Version: {platform.version()}")
    report.append("")

    # Environment Variables
    report.append("-" * 40)
    report.append("ENVIRONMENT VARIABLES")
    report.append("-" * 40)
    for key, value in sorted(os.environ.items()):
        # Mask sensitive values
        if any(s in key.lower() for s in ['token', 'key', 'secret', 'password', 'auth']):
            report.append(f"{key}=***MASKED***")
        else:
            report.append(f"{key}={value}")
    report.append("")

    # System Commands
    commands = [
        ("UNAME", "uname -a"),
        ("KERNEL", "cat /proc/version"),
        ("CPU INFO", "cat /proc/cpuinfo"),
        ("MEMORY INFO", "cat /proc/meminfo"),
        ("DISK USAGE", "df -h"),
        ("DISK PARTITIONS", "cat /proc/partitions"),
        ("MOUNT POINTS", "mount"),
        ("BLOCK DEVICES", "lsblk"),
        ("NETWORK INTERFACES", "ip addr"),
        ("NETWORK ROUTES", "ip route"),
        ("NETSTAT", "netstat -tuln"),
        ("SS SOCKETS", "ss -tuln"),
        ("IPTABLES", "iptables -L -n -v 2>/dev/null || echo 'iptables not accessible'"),
        ("UPTIME", "uptime"),
        ("LOAD AVG", "cat /proc/loadavg"),
        ("PROCESSES", "ps aux"),
        ("TOP SNAPSHOT", "top -bn1 | head -50"),
        ("OPEN FILES", "lsof 2>/dev/null | head -100 || echo 'lsof not available'"),
        ("SYSTEMD SERVICES", "systemctl list-units --type=service --state=running 2>/dev/null || echo 'systemctl not available'"),
        ("CRON JOBS", "crontab -l 2>/dev/null || echo 'No crontab for user'"),
        ("SYSTEM CRON", "ls -la /etc/cron.d/ 2>/dev/null"),
        ("SCHEDULED TASKS", "cat /etc/crontab 2>/dev/null"),
        ("USERS", "cat /etc/passwd"),
        ("GROUPS", "cat /etc/group"),
        ("SHADOW", "cat /etc/shadow 2>/dev/null || echo 'Permission denied'"),
        ("SUDOERS", "cat /etc/sudoers 2>/dev/null || echo 'Permission denied'"),
        ("LAST LOGIN", "last 2>/dev/null || echo 'last not available'"),
        ("WHO", "who"),
        ("W", "w"),
        ("FSTAB", "cat /etc/fstab"),
        ("HOSTS FILE", "cat /etc/hosts"),
        ("RESOLV CONF", "cat /etc/resolv.conf"),
        ("NSSWITCH", "cat /etc/nsswitch.conf"),
        ("SSH CONFIG", "cat /etc/ssh/sshd_config 2>/dev/null || echo 'sshd_config not found'"),
        ("INSTALLED PACKAGES (DPKG)", "dpkg -l 2>/dev/null || echo 'dpkg not available'"),
        ("INSTALLED PACKAGES (RPM)", "rpm -qa 2>/dev/null || echo 'rpm not available'"),
        ("INSTALLED PACKAGES (PACMAN)", "pacman -Q 2>/dev/null || echo 'pacman not available'"),
        ("PIP PACKAGES", "pip list 2>/dev/null || echo 'pip not available'"),
        ("NODE PACKAGES", "npm list -g 2>/dev/null || echo 'npm not available'"),
        ("DOCKER CONTAINERS", "docker ps -a 2>/dev/null || echo 'docker not available'"),
        ("DOCKER IMAGES", "docker images 2>/dev/null || echo 'docker not available'"),
        ("KUBECTL", "kubectl get all --all-namespaces 2>/dev/null || echo 'kubectl not available'"),
        ("SYSTEM LIMITS", "ulimit -a"),
        ("KERNEL PARAMETERS", "sysctl -a 2>/dev/null | head -200 || echo 'sysctl not available'"),
        ("DMESG", "dmesg 2>/dev/null | tail -100 || echo 'dmesg not available'"),
        ("JOURNALCTL", "journalctl --no-pager -n 100 2>/dev/null || echo 'journalctl not available'"),
        ("LOGGED IN USERS", "cat /var/run/utmp 2>/dev/null | strings | head -20 || echo 'utmp not readable'"),
        ("USB DEVICES", "lsusb 2>/dev/null || echo 'lsusb not available'"),
        ("PCI DEVICES", "lspci 2>/dev/null || echo 'lspci not available'"),
        ("HARDWARE INFO", "lshw 2>/dev/null | head -100 || echo 'lshw not available'"),
        ("DMIDECODE", "dmidecode 2>/dev/null | head -100 || echo 'dmidecode not available'"),
        ("LSMOD", "lsmod 2>/dev/null || echo 'lsmod not available'"),
        ("LSOF COUNT", "lsof 2>/dev/null | wc -l || echo 'lsof not available'"),
    ]

    for title, cmd in commands:
        report.append("-" * 40)
        report.append(title)
        report.append("-" * 40)
        report.append(run_cmd(cmd))
        report.append("")

    # File system walk
    report.append("-" * 40)
    report.append("DIRECTORY LISTINGS")
    report.append("-" * 40)

    dirs_to_list = [
        "/",
        "/home",
        "/etc",
        "/var",
        "/var/log",
        "/tmp",
        "/opt",
        "/usr",
        "/root",
        "/proc",
        "/sys",
        "/dev",
        "/run",
        "/boot",
    ]

    for directory in dirs_to_list:
        report.append(f"\n>>> {directory} <<<\n")
        report.append(run_cmd(f"ls -la {directory} 2>&1"))

    # Specific file contents
    report.append("\n" + "=" * 80)
    report.append("IMPORTANT FILE CONTENTS")
    report.append("=" * 80 + "\n")

    important_files = [
        "/etc/os-release",
        "/etc/lsb-release",
        "/etc/debian_version",
        "/etc/redhat-release",
        "/etc/hostname",
        "/etc/timezone",
        "/etc/localtime",
        "/etc/machine-id",
        "/etc/machine-info",
        "/etc/environment",
        "/etc/profile",
        "/etc/bash.bashrc",
        "/etc/profile.d/*",
        "/etc/security/limits.conf",
        "/etc/pam.d/*",
        "/etc/ld.so.conf",
        "/etc/modules",
        "/etc/modprobe.d/*",
        "/etc/sysctl.conf",
        "/etc/sysctl.d/*",
        "/etc/NetworkManager/*",
        "/etc/netplan/*",
        "/etc/network/*",
        "/etc/systemd/*",
        "/etc/init.d/*",
        "/var/log/syslog",
        "/var/log/messages",
        "/var/log/auth.log",
        "/var/log/kern.log",
        "/var/log/dmesg",
        "/var/log/boot.log",
        "/var/log/cron",
        "/var/log/maillog",
        "/var/log/wtmp",
        "/var/log/btmp",
        "/var/log/lastlog",
        "/var/log/dpkg.log",
        "/var/log/apt/*",
        "/var/log/yum.log",
        "/var/log/pacman.log",
        "/var/log/journal/*",
        "/proc/version",
        "/proc/cmdline",
        "/proc/config.gz",
        "/proc/devices",
        "/proc/interrupts",
        "/proc/iomem",
        "/proc/ioports",
        "/proc/dma",
        "/proc/cpuinfo",
        "/proc/meminfo",
        "/proc/swaps",
        "/proc/uptime",
        "/proc/stat",
        "/proc/loadavg",
        "/proc/modules",
        "/proc/filesystems",
        "/proc/mounts",
        "/proc/diskstats",
        "/proc/partitions",
        "/proc/net/*",
        "/proc/sys/*",
    ]

    for filepath in important_files:
        report.append(f"\n>>> {filepath} <<<\n")
        report.append(run_cmd(f"cat {filepath} 2>&1 | head -500"))

    # Python-specific info
    report.append("\n" + "=" * 80)
    report.append("PYTHON ENVIRONMENT")
    report.append("=" * 80 + "\n")

    report.append(f"Python executable: {sys.executable}")
    report.append(f"Python prefix: {sys.prefix}")
    report.append(f"Python path: {sys.path}")
    report.append(f"Modules loaded: {list(sys.modules.keys())[:50]}...")

    # Try to get pip freeze
    report.append("\n--- PIP FREEZE ---\n")
    report.append(run_cmd("pip freeze 2>/dev/null || pip3 freeze 2>/dev/null || echo 'pip not available'"))

    # Try to get conda info
    report.append("\n--- CONDA INFO ---\n")
    report.append(run_cmd("conda info 2>/dev/null || echo 'conda not available'"))
    report.append(run_cmd("conda list 2>/dev/null | head -50 || echo 'conda list not available'"))

    # Git info
    report.append("\n--- GIT INFO ---\n")
    report.append(run_cmd("git config --list 2>/dev/null || echo 'git not configured'"))
    report.append(run_cmd("git remote -v 2>/dev/null || echo 'not a git repo'"))
    report.append(run_cmd("git log --oneline -20 2>/dev/null || echo 'no git log'"))
    report.append(run_cmd("git status 2>/dev/null || echo 'git status not available'"))
    report.append(run_cmd("git branch -a 2>/dev/null || echo 'no branches'"))

    # Join and return
    return "\n".join(report)

def main():
    # Generate the report
    print("Gathering comprehensive system information...")
    report_content = gather_system_info()

    # Create filename with timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"system_audit_{hostname}_{timestamp}.txt"

    # Save to file
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(report_content)

    print(f"Report saved to: {filename}")
    print(f"Size: {os.path.getsize(filename)} bytes")

    # Also create a summary
    summary = f"""
AUDIT COMPLETE
==============
File: {filename}
Size: {os.path.getsize(filename)} bytes
Generated: {datetime.datetime.now().isoformat()}

Next steps:
1. Review the file: less {filename}
2. Add to git: git add {filename}
3. Commit: git commit -m "Add system audit report"
4. Push: git push origin main
"""
    print(summary)

if __name__ == "__main__":
    hostname = socket.gethostname()
    main()
