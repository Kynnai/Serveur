#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import threading
import socket
from xml.dom.minidom import parse, parseString
from protocoleJson import ProtocoleJson


class Serveur(threading.Thread , promt):

    PREFIXE_XML = "<?xml version=\"1.0\" ?>"
    serveur = None
    protocole = None
    interface = None
    nom = None
    dossier = None
    signature = None
    contenu = None
    date = None
    path = None
    rep = "DropBox"

    def __init__(self, threadName, connection, protocole, port, prompt):
        threading.Thread.__init__(self, name = threadName)
        self.connection = connection

    def run(self):
        dom = parseString("<monMessage>Merci de vous connecter</monMessage>")
        self.connection.send(bytes(dom.toxml(), 'UTF-8'))
        self.connection.close()

def run(protocole, port, prompt):
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
        cli = Serveur("Client " + str(nb_clients), connect, protocole, port, prompt)
        cli.start()
        nb_clients += 1

if __name__ == '__main__':
    if not os.path.isdir("DropBox"):
        os.mkdir("DropBox")
    prompt = False
    if "prompt" in sys.argv:
        prompt = True

    if sys.argv[2] == "json":
        run(ProtocoleJson, int(sys.argv[1]), prompt)

    elif sys.argv[2] == "xml":
        run(ProtocoleXml, int(sys.argv[1]), prompt)
