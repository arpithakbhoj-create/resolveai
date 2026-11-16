
import csv
from pathlib import Path

# Synthetic IT incident examples
incident_examples = {
    "Infrastructure": [
        "Windows server is not responding to remote desktop connections",
        "Virtual machine fails to start after scheduled maintenance",
        "Server CPU utilization remains above 95 percent",
        "Disk space is critically low on the application server",
        "Scheduled Windows patch installation failed",
        "Server operating system crashes during startup",
        "Virtual machine memory utilization is critically high",
        "Backup job failed on the production server",
    ],
    "Network": [
        
        "Users are unable to connect to the corporate VPN",
        "Network connection times out when accessing internal services",
        "DNS resolution fails for internal domain names",
        "Office network experiences frequent packet loss",
        "Router interface is down and causing connectivity issues",
        "Firewall routing configuration blocks network traffic",
        "Network latency is unusually high between data centers",
        "Wireless access points are frequently disconnecting users",
    
        "Employees cannot connect to VPN from home",
        "Remote employees are unable to establish VPN connection",
        "VPN client fails to authenticate remote users",
        "Corporate VPN connection disconnects frequently",
        "Users report VPN connectivity issues while working remotely",
        "Network connection fails when connecting from home",
        "VPN tunnel cannot be established",
        "Remote access VPN connection is unavailable",

 ],
    "Application": [
        "Web application displays an internal server error",
        "Application crashes when users submit a form",
        "Login page fails to load after application deployment",
        "Application API returns HTTP 500 errors",
        "Software service stops unexpectedly during processing",
        "Application response time increases after a new release",
        "Users cannot upload documents through the application",
        "Application authentication workflow fails for valid users",
    ],
    "Security": [
        "Multiple failed login attempts detected from unknown IP addresses",
        "Endpoint protection detects suspicious malware activity",
        "Unauthorized access attempt detected on a privileged account",
        "Security monitoring reports possible credential compromise",
        "Suspicious PowerShell execution detected on a workstation",
        "Potential phishing email reported by an employee",
        "Unusual outbound traffic indicates possible data exfiltration",
        "Critical security vulnerability detected on a server",
    ],
    "Database": [
        "Database queries are running significantly slower than expected",
        "SQL database connection pool is exhausted",
        "Database transaction fails due to a deadlock",
        "Database replication is delayed between primary and secondary",
        "Database backup fails during scheduled execution",
        "Application cannot connect to the SQL database",
        "Database storage utilization reaches critical capacity",
        "Database service stops unexpectedly after maintenance",
    ],
    "Other": [
        "Employee requests installation of approved office software",
        "User needs assistance configuring a new monitor",
        "Printer produces blank pages despite having sufficient toner",
        "Employee requests access to a shared team folder",
        "User reports an issue with a docking station",
        "Keyboard stops responding after connecting to a laptop",
        "Employee requests replacement of a damaged headset",
        "User needs help configuring an office desk phone",
        "Laptop keyboard is not working",
        "Several keys on the laptop keyboard have stopped responding",
        "Employee reports a faulty external keyboard",
        "Keyboard input is not detected by the laptop",
        "User requests replacement of a damaged laptop keyboard",
        "Wireless mouse stops responding intermittently",
        "Laptop touchpad is not functioning correctly",
        "Employee reports a malfunctioning USB headset",

    ],
}

output_path = Path(__file__).resolve().parent / "incidents.csv"

with open(output_path, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    writer.writerow(["description", "category"])

    for category, descriptions in incident_examples.items():
        for description in descriptions:
            writer.writerow([description, category])

print(f"Dataset created successfully: {output_path}")
print(f"Total incidents: {sum(len(v) for v in incident_examples.values())}")
print(f"Categories: {len(incident_examples)}")
