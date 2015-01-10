#!/usr/bin/env python

import os
import sys
import socket
import time
import serial

hostname = socket.gethostname()

interval = os.getenv("COLLECTD_INTERVAL") or 30
interval = float(interval)

instance = {"IINST": "intensite", "IMAX": "intensite", "ISOUSC": "intensite",
            "HCHC": "watt", "HCHP": "watt"}


def readTeleinfo():
    while ser.read(1) != chr(2):
        pass

    message = ""
    fin = False

    while not fin:
        char = ser.read(1)
        if char != chr(2):
            message = message + char
        else:
            fin = True

    trames = [
        trame.split(" ")
        for trame in message.strip("\r\n\x03").split("\r\n")
        ]
    return trames

try:
    ser = serial.Serial(
            port='/dev/ttyAMA0',
            baudrate=1200,
            parity=serial.PARITY_EVEN,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.SEVENBITS)
except:
    print sys.exc_info()
    sys.exit(1)

while True:
    ser.write('A')
    time.sleep(1)
    ser.flushInput()

    trames = readTeleinfo()

    for trame in trames:
        try:
            int(trame[1])
            print "PUTVAL %s/teleinfo-%s/power-%s interval=%i N:%s" %\
                    (hostname, instance.get(trame[0]), trame[0].lower(),
                            interval, int(trame[1]))
        except:
            print "value if label %s cannot be converted (%s)" %\
                    (trame[0], trame[1])

        time.sleep(interval)

ser.close()
