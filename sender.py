from scapy.all import Ether, IP, TCP, sendp, get_if_list, get_if_hwaddr, getmacbyip, conf

def build_and_send_tcp_layer2():
    # Configuration
    SRC_IP = "10.20.73.172"      # Your Windows IP
    DST_IP = "10.20.73.119"      # Mac receiver IP
    SRC_PORT = 12345
    DST_PORT = 4444
    
    # Get destination MAC address automatically
    try:
        dst_mac = getmacbyip(DST_IP)  # Scapy resolves MAC via ARP
        if dst_mac is None:
            print(f"Error: Cannot resolve MAC for {DST_IP}. Ensure device is reachable.")
            print("Try pinging it first: ping", DST_IP)
            return
    except Exception as e:
        print(f"MAC resolution failed: {e}")
        print("Manually set dst_mac to your Mac's MAC address (find via 'ifconfig' on Mac)")
        return
    
    # Show available interfaces
    print("Available interfaces:")
    print(get_if_list())
    print()
    
    # Build Layer 2 packet: Ethernet + IP + TCP + Data
    packet = (
        Ether(dst=dst_mac) /                              # Layer 2: Ethernet
        IP(src=SRC_IP, dst=DST_IP) /                      # Layer 3: IP
        TCP(sport=SRC_PORT, dport=DST_PORT, flags='S',    # Layer 4: TCP
            seq=1000, ack=0, window=2048) /
        b'Hello from Windows!'                            # Payload
    )
    
    print("--- Packet Built (Layer 2) ---")
    packet.show()
    
    print(f"\nSending packet to {DST_IP} (MAC: {dst_mac})...")
    
    # Send using Layer 2 (sendp) - this bypasses Windows raw socket restriction
    sendp(packet, verbose=1)
    
    print("Packet sent successfully via Layer 2!")

def main():
    # Configure Scapy to use Npcap (should auto-detect after install)
    print(f"Using Npcap: {conf.use_pcap}")
    print()
    
    build_and_send_tcp_layer2()

if __name__ == "__main__":
    main()
