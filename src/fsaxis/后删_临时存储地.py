import socket
import psutil

def get_ipv4_address(adapter_name):
    adapters = psutil.net_if_addrs()
    for name, snics in adapters.items():
        if name == adapter_name:
            for snic in snics:
                if snic.family == socket.AF_INET:
                    return snic.address
    return "Adapter not found or doesn't have an IPv4 address."

# Replace 'WLAN' with the exact name of your wireless adapter
ipv4_address = get_ipv4_address('WLAN')
print("IPv4 Address:", ipv4_address)
