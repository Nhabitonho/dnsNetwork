import socket
import platform
import os
import re
import subprocess

system = platform.system()

def get_default_gateway():
    if system == "Darwin":
        result = str(subprocess.check_output(["route", "get", "default"]))
        start = 'gateway: '
        end = '\\n'
        if 'gateway' in result:
            return (result.split(start))[1].split(end)[0]
    elif system == "Windows":
        result = str(subprocess.check_output(["ipconfig"]))
        start = 'Default Gateway . . . . . . . . . : '
        end = 'Ethernet'
        if 'Default Gateway' in result:
            gateWayStr = result.split(start)[1].split(end)[0]
            gateWayStr = re.sub(r'\\r\\n|\\r\\n\\r\\n', ' ', gateWayStr)
            return gateWayStr
    else : print("Error !!")

def get_dns_server():
    if system == "Darwin":
        dns_servers = []
        with open('/etc/resolv.conf') as f:
            for line in f:
                if line.startswith('nameserver'):
                    dns_servers.append(line)
            ip_addresses = [line.split()[1] for line in dns_servers if line.startswith('nameserver')]
            result = ', '.join(ip_addresses)
            return result
    elif system == "Windows":
        route_dns_result = str(subprocess.check_output(["ipconfig", "/all"]))
        start = 'DNS Servers . . . . . . . . . . . : '
        end = 'Primary'
        if 'DNS Servers' in route_dns_result:
            dnsStr = route_dns_result.split(start)[1].split(end)[0]
            dnsStr = dnsStr.replace('\\r\\n', '').strip()
            dnsStr = dnsStr.replace('\t', '\n')
        return dnsStr
    else: "Error"
def get_google_ip():
    ip = socket.gethostbyname('google.com')
    return ip

if __name__ == "__main__":
    default_gateway = get_default_gateway()
    dns_server = get_dns_server()
    google_ip = get_google_ip()

    print(f"Default Gateway: {default_gateway}")
    print(f"DNS Server: {dns_server}")
    print(f"IP Address of google.com: {google_ip}")