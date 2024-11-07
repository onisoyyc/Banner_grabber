# Port Scanner

This Python script performs a multi-threaded scan on a range of ports for a specified IP address, grabs banners from open ports to identify services, and checks for known exploits using `searchsploit`. The program generates a report of the results, including open ports, service banners, and exploitability information, saved to a timestamped file.

## Features

- **Port Scanning**: Scans a specified range of ports to identify open ones.
- **Banner Grabbing**: Attempts to retrieve service information from open ports.
- **Exploitability Check**: Uses `searchsploit` to find potential vulnerabilities related to detected services.
- **Threading for Speed**: Scans ports concurrently using multiple threads to reduce scan time.
- **Output Report**: Saves scan results in a file with a timestamp for easy reference.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/port-scanner.git
   cd port-scanner
   ```

2. Install required Python packages:
   ```bash
   pip install requests
   ```

3. Install `searchsploit` (part of the `exploit-db` package):
   ```bash
   sudo apt update
   sudo apt install exploitdb
   ```

## Usage

Run the script with the following arguments:
```bash
python port_scanner.py <IP_ADDRESS> <START_PORT> <END_PORT>
```

### Example
```bash
python port_scanner.py 192.168.1.1 20 1000
```

## Output

The program outputs results both to the console and to a timestamped text file (e.g., `bannergrab_01012023_1234.txt`). The report includes:
- IP address and port details
- Service banner or service name
- `searchsploit` results for potential exploits

## Script Details

### Common Ports
The script scans commonly used ports and includes a dictionary of port numbers with typical service names:
```python
COMMON_PORTS = {
    21: "ftp", 22: "ssh", 23: "telnet", 25: "smtp",
    53: "dns", 80: "http", 110: "pop3", 143: "imap",
    443: "https", 3306: "mysql", 3389: "rdp", 5900: "vnc",
    6379: "redis", 8080: "http-proxy"
}
```

### Main Functions

1. **Port Scanning**: Uses a `Queue` and threads to scan ports in the specified range.
2. **Banner Grabbing**: Attempts to identify services by grabbing banners from the HTTP server or receiving data over a socket.
3. **Exploitability Check**: Runs `searchsploit` with the identified service name or banner information to find potential exploits.

## Requirements

- Python 3.6+
- `requests` library
- `searchsploit` tool

## Notes

- **Execution Time**: The scan can take a few minutes depending on the range of ports and the target system's response time.
- **Accuracy**: Not all services will respond with banners; some ports may be detected as open but provide limited or no service information.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

Enjoy using this port scanner for network security assessments and research.
