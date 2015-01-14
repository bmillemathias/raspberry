#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Code de collecte des information de telemetrie d'un compteur electrique, base sur
# http://www.domotique-info.fr/wp-content/uploads/2013/06/teleinfo-mysql.py_.txt

import os
import sys
import socket
import time
import serial

DEFAULT_SERIAL = "/dev/ttyAMA0"

hostname = socket.gethostname()

interval = os.getenv("COLLECTD_INTERVAL") or 30
interval = float(interval)

instance = {"IINST": "intensite", "IMAX": "intensite", "ISOUSC": "intensite",
            "HCHC": "watt", "HCHP": "watt"}

try:
    serial_device = sys.argv[1]
except:
    serial_device = DEFAULT_SERIAL


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
            port=serial_device,
            baudrate=1200,
            parity=serial.PARITY_EVEN,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.SEVENBITS)
except:
    print "Unable to open device %s" % serial_device
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
