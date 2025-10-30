from scapy.all import sniff, Ether, IP, TCP

def packet_handler(packet):
    if IP in packet and TCP in packet:
        ip = packet[IP]
        tcp = packet[TCP]
        
        print("\n" + "="*60)
        print("TCP PACKET RECEIVED!")
        print("="*60)
        print(f"Source IP/Port:      {ip.src}:{tcp.sport}")
        print(f"Destination IP/Port: {ip.dst}:{tcp.dport}")
        print(f"Sequence Number:     {tcp.seq}")
        print(f"Acknowledgment:      {tcp.ack}")
        print(f"Flags:               {tcp.flags}")
        print(f"Window Size:         {tcp.window}")
        print(f"Checksum:            0x{tcp.chksum:04x}")
        
        # Display payload if present
        if packet.haslayer('Raw'):
            payload = packet['Raw'].load
            print(f"Payload:             {payload}")
        
        print("\n--- Raw Hex Dump ---")
        packet.show()
        print("="*60)

def main():
    print("Listening for TCP packets on port 4444...")
    print("Press Ctrl+C to stop\n")
    
    # Sniff for TCP packets on port 4444
    sniff(filter="tcp port 4444", prn=packet_handler, store=0)

if __name__ == "__main__":
    main()