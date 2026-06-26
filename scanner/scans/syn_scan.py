from scapy.layers.inet import IP, TCP
from scapy.sendrecv import sr1, send

ip = "127.0.0.1"

i = int(input("Enter your port: "))

response = sr1(IP(dst=ip)/TCP(dport=i, flags="S"), timeout=2, verbose=0)

if response is None:
    print("port filtered")
elif response.haslayer(TCP):
    if response[TCP].flags == "SA":
        print(f"port {i} is open")
        send(IP(dst=ip)/TCP(dport=i, flags="R"), verbose=0)
    elif response[TCP].flags == "RA" or response[TCP].flags == "R":
        print(f"port {i} closed")
