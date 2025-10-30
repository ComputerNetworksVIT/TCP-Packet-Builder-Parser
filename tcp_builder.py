from scapy.all import IP, TCP

def build_tcp_packet(target_ip, source_port, dest_port, flags, seq_num, ack_num, payload=""):
    """
    Constructs a valid TCP packet using Scapy.
    
    Args:
        target_ip (str): The destination IP address.
        source_port (int): The source port number.
        dest_port (int): The destination port number.
        flags (str): A string of TCP flags (e.g., 'S' for SYN, 'FA' for FIN+ACK).
        seq_num (int): The sequence number.
        ack_num (int): The acknowledgment number.
        payload (str): Optional data to include in the packet.
        
    Returns:
        A Scapy packet object.
    """
    # Create an IP layer. Scapy will fill in the source IP automatically.
    ip_layer = IP(dst=target_ip)
    
    # Create a TCP layer.
    tcp_layer = TCP(
        sport=source_port,
        dport=dest_port,
        flags=flags,
        seq=seq_num,
        ack=ack_num,
        window=2048 # Sets the 16-bit window size field [cite: 32]
    )
    
    # Combine the layers and add the payload.
    # Scapy will automatically calculate the checksum upon sending.
    packet = ip_layer/tcp_layer/payload
    
    print("--- Packet Built ---")
    packet.show() # Display a summary of the built packet
    
    return packet