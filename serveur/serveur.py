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
        self.path = os.path.dirname(os.path.abspath(__file__))
        self.protocole = protocole
        self.serveur = Serveur(port)
        self.interface = InterfaceUtilisateur()
        if prompt:
            self.communication()
        else:
            self.synchroniser(self.rep, "./")

    def communication(self):
        r = self.interface.lecteur()
        while r[0] != "quitter":
            envoie = None
            message = "Commande invalide"
            if r[0] == "connecter?":
                envoie = self.protocole.genere_bonjour(self)
            elif r[0] == "nomServeur?":
                envoie = self.protocole.genere_nom(self)
            elif r[0] == "listeDossier?":
                if len(r) != 1:
                    envoie = self.protocole.genere_listeDossiers(self, r[1])
                else:
                    envoie = self.protocole.genere_listeDossiers(self, "./")
            elif len(r) != 1:
                if r[0] == "dossier?":
                    self.interface.retourMessageServeur(self.dossierExist(r[1]))
                elif r[0] == "creerDossier?":
                    envoie = self.protocole.genere_creerDossier(self, r[1])
                elif r[0] == "televerser?":
                    self.initialiserInformationComplexe(r[1])
                    envoie = self.protocole.genere_televerserFichier(self, self.nom, self.dossier, self.signature,
                                                                     self.contenu, self.date)
                elif r[0] == "telecharger?":
                    self.telecharger(r[1])
                    self.interface.retourMessageServeur("OK")
                elif r[0] == "supprimerDossier?":
                    envoie = self.protocole.genere_supprimerDossier(self, r[1])
                elif r[0] == "supprimerFichier?":
                    self.initialiserInformationDeBase(r[1])
                    envoie = self.protocole.genere_supprimerFichier(self, self.nom, self.dossier)
                elif r[0] == "fichier?":
                    self.initialiserInformationDeBase(r[1])
                    envoie = self.protocole.genere_listeFichiers(self, self.dossier)
                    if self.nom != self.dossier:
                        self.serveur.send(envoie)
                        message_serveur = self.serveur.receive()
                        retourInterprete = (self.protocole.interprete(self, message_serveur)).split(" ")
                        if self.nom in retourInterprete:
                            self.interface.retourMessageServeur("oui")
                        else:
                            self.interface.retourMessageServeur("non")
                elif r[0] == "identiqueFichier?" or r[0] == "fichierIdentique?" or r[0] == "telecharger?":
                    self.initialiserInformationComplexe(r[1])
                    envoie = self.protocole.genere_fichierIdentique(self, self.nom, self.dossier, self.signature,
                                                                    self.date)
                elif r[0] == "fichierRecent?":
                    self.initialiserInformationComplexe(r[1])
                    envoie = self.protocole.genere_fichierRecent(self, self.nom, self.dossier, self.date)
                elif r[0] == "miseAjour":
                    self.miseAjour(r[1])
            elif r[0] == "quitter":
                envoie = self.protocole.genere_quitter(self)
            else:
                message = "Élément manquant!"

            if envoie != None and r[0] != "telecharger?" and r[0] != "miseAjour" and r[0] != "dossier?":
                self.serveur.send(envoie)
                message_serveur = self.serveur.receive()
                self.interface.retourMessageServeur(self.protocole.interprete(self, message_serveur))
            elif r[0] == "telecharger?" or r[0] == "fichier?" or r[0] == "miseAjour" or r[0] == "dossier?":
                pass
            else:
                self.interface.retourMessageServeur(message)

            r = input("Commande:").split(" ")
        self.interface.retourMessageServeur("bye")

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
