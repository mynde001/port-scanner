# Port Scanner

import socket
import threading
import time

IP = str(input("Enter IPv4 address: "))

num_of_ports = 1023
current_port = 0
open_ports = []
threads = []

print("Scanning...")
start = time.time()

def port_scanner(current_port):
    with socket.socket() as s:
        try:
            s.connect((IP, current_port))
            open_ports.append(current_port)
        except:
            pass

for _ in range(num_of_ports):
    thread = threading.Thread(target=port_scanner, args=(current_port,))
    thread.start()
    threads.append(thread)
    current_port += 1

# Waits for all threads to finish
for thread in threads:
    thread.join()

finish = time.time()

for port in open_ports:
    print(f"Port {port} is open")

print(f"The process took {int(finish - start)} seconds to complete")