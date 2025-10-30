# TCP Packet Builder & Parser

This project provides a set of Python scripts to build, send, receive, and parse TCP packets using the Scapy library. It is designed for cross-platform execution between a Windows sender and a macOS receiver, demonstrating fundamental concepts of network programming and the TCP/IP protocol suite as defined in RFC 9293.

## Features

-   **RFC 9293 Compliant**: Constructs TCP packets with all required header fields.
-   **Full Flag Support**: Crafts packets with any combination of TCP flags (SYN, ACK, FIN, RST, PSH, URG, CWR, ECE).
-   **Cross-Platform**: Designed for sending from Windows and receiving on macOS.
-   **Layer 2 Sending**: Uses Layer 2 (Ethernet) packet construction to bypass Windows raw socket restrictions.
-   **Real-Time Parsing**: The receiver script captures packets live and provides a detailed breakdown of headers.
-   **Checksum Validation**: Automatically validates the integrity of received TCP packets.

## File Structure

The project is organized into a modular architecture:

```
.
├── sender.py           # Main script to send packets (Windows)
├── receiver.py         # Main script to receive packets (macOS)
└── tcp_builder.py      # (Optional) A modular library for building TCP packets
```

-   **`sender.py`**: The primary script for the sending machine. It resolves the destination MAC address, constructs a complete Layer 2 (Ethernet) frame containing the IP and TCP segments, and transmits it.
-   **`receiver.py`**: The primary script for the receiving machine. It sniffs the network for incoming TCP packets on a specific port, parses the headers, validates the checksum, and prints a detailed analysis.
-   **`tcp_builder.py`**: A helper module that provides a function to construct TCP packets. While `sender.py` contains its own logic, this module can be used for other testing scenarios.

---

## Prerequisites

### 1. System Requirements
-   **Two machines** on the same local network (e.g., connected to the same Wi-Fi router).
    -   **Sender**: Windows 10/11
    -   **Receiver**: macOS
-   Python 3.8+ installed on both machines.

### 2. Dependencies
Install the necessary Python library on both systems:

```
pip install scapy
```

### 3. Windows-Specific Setup (Sender Machine)
Scapy requires a special driver on Windows to perform raw packet operations.

1.  **Download Npcap**: Go to the official [Npcap website](https://npcap.com/#download) and download the latest installer.
2.  **Install Npcap**: Run the installer **as Administrator** and ensure the following option is checked during installation:
    -   `Install Npcap in WinPcap API-compatible Mode`
3.  **Restart** your computer after the installation is complete.

---

## Execution Guide

Follow these steps to run the project.

### Step 1: Configure the Scripts

1.  **Find IP Addresses**:
    -   On the **Windows** machine (Sender), open Command Prompt and run `ipconfig`. Note the IPv4 address.
    -   On the **macOS** machine (Receiver), open Terminal and run `ifconfig | grep "inet "`. Note the IP address.

2.  **Edit `sender.py`**:
    -   Open `sender.py` in a text editor.
    -   Update the `SRC_IP` and `DST_IP` variables with the IP addresses you found.

    ```
    # sender.py
    SRC_IP = "192.168.1.10"  # Your Windows IP
    DST_IP = "192.168.1.15"  # Your Mac IP
    ```

### Step 2: Run the Receiver (macOS)

On the macOS machine, open a Terminal window and run the `receiver.py` script with `sudo` to grant it the necessary permissions to sniff network packets.

```
# Navigate to the project directory
cd /path/to/your/project

# Run the script with root privileges
sudo python receiver.py
```

The terminal will display `Listening on TCP port 4444...` and wait for an incoming packet.

### Step 3: Run the Sender (Windows)

On the Windows machine, you must run the script from a Command Prompt with elevated privileges.

1.  Click the **Start Menu**, type `cmd`.
2.  Right-click on **Command Prompt** and select **"Run as administrator"**.
3.  In the administrator Command Prompt, navigate to your project directory.

    ```
    cd C:\path\to\your\project
    ```

4.  Execute the `sender.py` script.

    ```
    python sender.py
    ```

### Step 4: Observe the Results

-   **On the Sender (Windows)**, you will see output confirming the packet was built and sent:

    ```
    --- Packet Built (Layer 2) ---
    ###[ Ethernet ]###
      dst= aa:bb:cc:dd:ee:ff
    ###[ IP ]###
      src= 192.168.1.10
      dst= 192.168.1.15
    ...
    Sent 1 packets.
    ```

-   **On the Receiver (macOS)**, the script will immediately print the parsed details of the received packet:

    ```
    --- TCP Packet Received ---
    Source IP: 192.168.1.10
    Destination IP: 192.168.1.15
    Source Port: 12345
    Dest. Port: 4444
    Sequence Num: 1000
    Flags: S
    Window Size: 2048
    Checksum: 0xabcd (Valid)
    Payload: Hello from Windows!
    ```

## Troubleshooting

-   **Permission Denied / WinError 10013**: You did not run the script as an administrator (Windows) or with `sudo` (macOS).
-   **`Scapy_Exception: No libpcap provider available`**: Npcap is not installed correctly on Windows. Re-install it, ensuring the "WinPcap API-compatible mode" is enabled, and restart your PC.
-   **No Packet Received**:
    -   Verify that both IP addresses are correct and both devices are on the same network.
    -   Temporarily disable the firewall on both the sender and receiver to ensure it is not blocking the packets.
    -   Ensure the `DST_IP` in `sender.py` is reachable. Try running `ping <DST_IP>` from the sender machine.
```
