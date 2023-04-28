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
from queue import Queue

q = Queue()

# Initializes the app again once finished
while 1:
    ADDRESS = str(input("Enter IP or Domain address: "))
    num_of_ports = int(input("Enter the amount of ports (defaults are: 1. WKP: 0 - 1023, 2. RP: 1024 - 49151): "))
    timeout = int(input("Seconds before connection times out (default is 3): ") or "3")

    # Range loop starting integer
    num_of_ports_start = 0

    # Amount of ports (to and from) based on num_of_ports input (1/2)
    if num_of_ports == 1:
        num_of_ports = 1024
    elif num_of_ports == 2:
        num_of_ports_start = 1024
        num_of_ports = 49152

    finish = None
    open_ports = []
    threads = []

    # Queues ports
    for i in range(num_of_ports_start, num_of_ports):
        q.put(i)

    scanning_text = f"> Scanning {ADDRESS}"

    # Adds dots to the end of scanning_text as the address is being scanned for ports
    def text_dots():
        counter = 0
        # global allows for modifying a global variable from local context
        global scanning_text

        while finish == None:
            if counter != 4:
                counter += 1
                print("\r" + scanning_text, end="")
                scanning_text += "."
                time.sleep(0.3)
            elif counter >= 4:
                scanning_text = scanning_text[:-4]
                counter = 0

    text_dot_thread = threading.Thread(target=text_dots)
    text_dot_thread.start()

    start = time.time()

    def port_scanner(port):
        with socket.socket() as s:
            s.settimeout(timeout)

            try:
                s.connect((ADDRESS, port))
                open_ports.append(port)
            except:
                pass

    def worker():
        while not q.empty():
            port = q.get()
            port_scanner(port)

    def threader(start, end):
        for _ in range(start, end):
            thread = threading.Thread(target=worker)
            thread.start()
            threads.append(thread)

    threader(num_of_ports_start, num_of_ports)

    # Waits for all threads to finish before outputting the result
    for thread in threads:
        thread.join()

    finish = time.time()

    # Whitespace
    print(" ")

    for port in open_ports:
        print(f"> Port {port} is open")

    print(f'''The process took {int(finish - start)} seconds to complete
    ''')