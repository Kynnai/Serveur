#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import threading
import socket
from xml.dom.minidom import parse, parseString


class Serveur(threading.Thread):
    def __init__(self, threadName, connection):
        threading.Thread.__init__(self, name = threadName)
        self.connection = connection

    def run(self):
        dom = parseString("<monMessage>Merci de vous connecter</monMessage>")
        self.connection.send(bytes(dom.toxml(), 'UTF-8'))
        self.connection.close()

s = socket.socket()
host = ''
port = 50000
s.bind((host, port))
s.listen(5)

nb_clients = 0

while True:
    print("Attente d'un autre client...")
    connect, addr = s.accept()
    print ('Connexion venant de ', addr)
    cli = Serveur("Client " + str(nb_clients), connect)
    cli.start()
    nb_clients += 1