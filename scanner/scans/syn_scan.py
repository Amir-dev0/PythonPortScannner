from scapy.layers.inet import IP, TCP
from scapy.sendrecv import sr1, send

TARGET = "127.0.0.1"

def single_scan(port:int):
    response = sr1(IP(dst=TARGET)/TCP(dport=port, flags="S"), timeout=2, verbose=0)

    if response is None:
        print("port filtered")
    elif response.haslayer(TCP):
        if response[TCP].flags == "SA":
            print(f"port {port} is open")
            send(IP(dst=TARGET)/TCP(dport=port, flags="R"), verbose=0)
        elif response[TCP].flags == "RA" or response[TCP].flags == "R":
            print(f"port {port} closed")

def range_scan(begin:int, end:int):
    for port in range(begin, end + 1):
        response = sr1(IP(dst=TARGET)/TCP(dport=port, flags="S"), timeout=2, verbose=0)
        if response is None:
            print("port filtered")
        elif response.haslayer(TCP):
            if response[TCP].flags == "SA":
                print(f"port {port} is open")
                send(IP(dst=TARGET)/TCP(dport=port, flags="R"), verbose=0)
            elif response[TCP].flags == "RA" or response[TCP].flags == "R":
                print(f"port {port} closed")    