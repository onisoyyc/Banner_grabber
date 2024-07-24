#Port scanner 
#The program takes a little bit so let it run for a few minutes
#It will eventually print the results and create a new file with timestamp.

import socket 
import requests #For HTTP server request and response functions
from datetime import datetime
import subprocess
import argparse
import threading
from queue import Queue


# Common ports and their typical services
COMMON_PORTS = {
    21: "ftp",
    22: "ssh",
    23: "telnet",
    25: "smtp",
    53: "dns",
    80: "http",
    110: "pop3",
    143: "imap",
    443: "https",
    3306: "mysql",
    3389: "rdp",
    5900: "vnc",
    6379: "redis",
    8080: "http-proxy"
}

def scan_port(ip, port, open_ports):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    result = sock.connect_ex((ip, port))
    if result == 0:
        open_ports.append(port)
        sock.close()

def worker(ip, port_range, open_ports):
    while True:
        port = port_range.get()
        if port is None:
            break
        scan_port(ip, port, open_ports)
        port_range.task_done()

def scan_ports(ip, port_range, num_threads=100):
    open_ports = [] #create a list of open ports
    queue = Queue() #create lock
    threads = []

    for port in range(port_range[0], port_range[1] + 1):
        queue.put(port)

    for _ in range(num_threads):
        thread = threading.Thread(target=worker, args=(ip, queue, open_ports))
        thread.start()
        threads.append(thread)

    queue.join()

    for _ in range(num_threads):
        queue.put(None)
    for thread in threads:
        thread.join()

    return open_ports
    # pre threading code
    # for port in range(port_range[0], port_range[1] + 1):
    #     #create a new socket object
    #     sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #     sock.settimeout(1)
    #     #attempt to connect the the sever
    #     result = sock.connect_ex((ip, port)) # returns an errno instead of raising exception
    #     if result == 0: #successful connection
    #         open_ports.append(port)
    #         print("Connection successful on port: ",port)
    #     #TESTING
    #     #else:
    #         #print(f"Connection failed with error code: {result}")
    #     sock.close()
    # return open_ports


def grab_banner(ip, port):
    #attempt check if server is running on http ports and retrieve the server's header info
    try:
        if port in [80, 443, 8080, 8000]:
            #Send HEAD request to the specified IP address and port
            response = requests.head(f"http://{ip}:{port}", timeout=2)
            #attempt retrieval of server header from response, if not present return HTTP Service
            return response.headers.get('Server', 'HTTP Service')
        else:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            sock.connect((ip, port))
            #Recieve upto 1024 bytes of data from socket, decode, and strip any whitespaces
            banner = sock.recv(1024).decode().strip()
            sock.close()
            return banner
        #catch exceptions that occur in try block
    except Exception as e:
        return str(e)


#auto use searchsploit function
def check_exploitability(port, banner):
    #use subprocess.run method to executre the searchsploit command 
    # Use the banner if available, otherwise use common port service name
    service_name = banner or COMMON_PORTS.get(port, "unknown")
    result = subprocess.run(['searchsploit', service_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    output = result.stdout + result.stderr
    if 'No Results' in output:
        return False, output
    return True, output


def main(ip, port_range):
    open_ports = scan_ports(ip, port_range)
    services = []

    for port in open_ports:
        banner = grab_banner(ip, port)
        if banner:
            exploitable, exploit_info = check_exploitability(port, banner)
            services.append((ip, port, banner, exploitable, exploit_info))

    #Print and write results to file
    timestamp = datetime.now().strftime("%m%d%Y_%H%M")
    filename = f"bannergrab_{timestamp}.txt"
    
    with open(filename, 'w') as file:
        for service in services:
            ip, port, banner, exploitable, exploit_info = service
            result = (
                f"==============================\n"
                f"IP address: {ip}\n"
                f"Port: {port}\n"
                f"Banner: {banner}\n"
                f"SearchSploit:\n"
                #f"{'Exploitable' if exploitable else 'Not Exploitable'}\n\n"
                f"Exploits:\n{exploit_info}\n"
                f"==============================\n"
            )
            print(result)
            file.write(result + "\n")

if __name__ == "__main__":
    #take commands form the comamand line
    parser = argparse.ArgumentParser(description="Python Banner Grabber\n Author:Daniel Osah")
    parser.add_argument("ip", help="Target IP address")
    parser.add_argument("start_port", type=int, help="Starting port number")
    parser.add_argument("end_port", type=int, help="Ending port number")

    args = parser.parse_args()

    ip = args.ip
    port_range = (args.start_port, args.end_port)
    main(ip, port_range)

