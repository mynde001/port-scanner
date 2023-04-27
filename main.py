print('''
  _____           _      _____
 |  __ \         | |    / ____|
 | |__) |__  _ __| |_  | (___   ___ __ _ _ __  _ __   ___ _ __
 |  ___/ _ \| '__| __|  \___ \ / __/ _` | '_ \| '_ \ / _ \ '__|
 | |  | (_) | |  | |_   ____) | (_| (_| | | | | | | |  __/ |
 |_|   \___/|_|   \__| |_____/ \___\__,_|_| |_|_| |_|\___|_|

WKP - System or well-known ports
Well-known ports are port numbers that have been reserved for common applications, typically server applications

RP - User or registered ports
A registered port is a network port designated for use with a certain protocol or application

To choose either of the 2, enter 1 or 2 respectively or enter a custom amount
''')

import socket
import threading
import time

# Initializes the app again once finished
while 1:
    ADDRESS = str(input("Enter IP or Domain address: "))
    num_of_ports = int(input("Enter the amount of ports (defaults are: 1. WKP: 0 - 1023, 2. RP: 1024 - 49151): "))
    timeout = int(input("Seconds before connection times out (default is 21): ") or "21")

    # Thread range loop start
    range_start = 0

    # Amount of ports (to and from) based on num_of_ports input (1/2)
    if num_of_ports == 1:
        num_of_ports = 1024
    elif num_of_ports == 2:
        range_start = 1024
        num_of_ports = 49152

    current_port = 0
    open_ports = []
    threads = []

    print(f"> Scanning {ADDRESS}...")

    start = time.time()

    def port_scanner(current_port):
        with socket.socket() as s:
            s.settimeout(timeout)

            try:
                s.connect((ADDRESS, current_port))
                open_ports.append(current_port)
            except:
                pass

    for _ in range(range_start, num_of_ports):
        thread = threading.Thread(target=port_scanner, args=(current_port,))
        thread.start()
        threads.append(thread)
        current_port += 1

    # Waits for all threads to finish before outputting the result
    for thread in threads:
        thread.join()

    finish = time.time()

    for port in open_ports:
        print(f"> Port {port} is open")

    print(f'''The process took {int(finish - start)} seconds to complete
    ''')