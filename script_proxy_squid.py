#!/usr/share/python3 

import sys, signal, requests

def def_handler(sig, frame):
    print("\n\n[!] Saliendo...\n")
    sys.exit(1)
 
# Ctrl-C
signal.signal(signal.SIGINT, def_handler)

main_url = "http://127.0.0.1"
squid_proxy = {'http': 'http://192.168.0.102:3128'}


def portDiscovery ():
    common_tcp_ports = {21, 22, 23, 25, 53, 80, 110, 115, 119, 123, 143, 161, 194, 443, 465, 514, 587, 993, 995, 1080, 1433, 1434, 1521, 1723, 3306, 3389, 5432, 5900, 8080, 8443, 8888, 9100, 9999, 10000, 11211, 27017, 28017, 50000, 50070, 50075, 54321, 5984, 6379, 6666, 7070, 8081}

    for tcp_port in common_tcp_ports:
        r = requests.get(main_url + ':' + str(tcp_port), proxies=squid_proxy)

        if r.status_code != 503:
            print("\n[+] Port " + str(tcp_port) + " - OPEN")

if __name__ == '__main__':
    portDiscovery()