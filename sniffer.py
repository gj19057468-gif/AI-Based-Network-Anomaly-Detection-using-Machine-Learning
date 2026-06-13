from scapy.all import sniff
from scapy.layers.inet import IP
import csv
from datetime import datetime

csv_file = "network_traffic.csv"

with open(csv_file, "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow([
        "Timestamp",
        "Source_IP",
        "Destination_IP",
        "Protocol",
        "Packet_Size"
    ])

def process_packet(packet):
    if IP in packet:

        timestamp = datetime.now()

        src_ip = packet[IP].src
        dst_ip = packet[IP].dst

        protocol = packet[IP].proto
        packet_size = len(packet)

        with open(csv_file, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([
                timestamp,
                src_ip,
                dst_ip,
                protocol,
                packet_size
            ])

        print(
            f"Source: {src_ip} | "
            f"Destination: {dst_ip} | "
            f"Protocol: {protocol} | "
            f"Size: {packet_size}"
        )

print("Capturing packets...")

sniff(prn=process_packet, count=50)

print("Capture completed.")