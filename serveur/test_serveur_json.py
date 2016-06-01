#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from unittest import TestCase
from serveur.protocoleJson import ProtocoleJson

class testjson_serveur_json(TestCase):

    def setUp(self):
        self.protocole = ProtocoleJson()

    def testjson_bonjour(self):
        self.assertTrue(self.protocole.interprete('{"salutation": "bonjourServeur"}'), json.dumps({"salutation": "bonjourClient"}))

    def testjson_nomServeur(self):
        self.assertTrue(self.protocole.interprete('{"action": "questionNomServeur"}'), json.dumps({"nomServeur": "Ubuntu Dropbox 1.0"}))

    def testjson_listeDossier(self):
        self.assertTrue(self.protocole.interprete('{"questionListeDossiers": "d1"}'), json.dumps({"listeDossiers": {"dossier": ["d1/d2"]}}))

    #IF
    def testjson_listeDossierInexistant(self):
        self.assertTrue(self.protocole.interprete('{"questionListeDossier": "d1"}'), json.dumps({"reponse": "erreurDossierInexistant"}))

    def testjson_listeFichiers(self):
        self.assertTrue(self.protocole.interprete('{"questionListeFichiers": "d1"}'), json.dumps({"listeFichiers": {"fichier": ["d1/f1"]}}))

    #IF
    def testjson_listeFichiersMaisDossierInexistant(self):
        self.assertTrue(self.protocole.interprete('{"questionListeFichiers": "d20"}'), json.dumps({"reponse": "erreurDossierInexistant"}))

    #A REGARDER (IF)
    def testjson_listeFichiersMaisDossierLecture(self):
        #self.assertTrue(self.protocole.interprete('{"questionListeFichiers": "d1"}'), json.dumps({"reponse": "erreurDossierLecture"}))
        pass

    def testjson_creerDossier(self):
        self.assertTrue(self.protocole.interprete('{"creerDossier": "d7/d8/d9"}'), json.dumps({"reponse": "ok"}))

    #IF
    def testjson_creerDossierDejaExistant(self):
        self.assertTrue(self.protocole.interprete('{"creerDossier": "d7/d8/d9"}'), json.dumps({"reponse": "erreurDossierExiste"}))

    #IF
    def testjson_creerDossierDansRepertoirNonExistant(self):
        self.assertTrue(self.protocole.interprete('{"creerDossier": "d10/d11"}'), json.dumps({"response": "erreurDossierInexistant"}))

    def testjson_televerserFichier(self):
        self.assertTrue(self.protocole.interprete(json.dumps({"televerserFichier": {"nom": "a1", "dossier": "b2", "signature": "c3", "contenu": "d4", "date": "2016/04/19"}})), json.dumps({"reponse": "ok"}))

    #IF
    def testjson_televerserFichierFichierDejaExistant(self):
        self.assertTrue(self.protocole.interprete(json.dumps({"televerserFichier":{"nom": "a1", "dossier": "b2", "signature": "c3", "contenu": "d4", "date": "2016/04/19"}})), json.dumps({"reponse": "erreurFichierExiste"}))

    def testjson_telechargerFichier(self):
        self.assertFalse(self.protocole.interprete(json.dumps({"telechargerFichier":{"nom": "f2", "dossier": "d1"}})), json.dumps({"reponse": "erreurDossierInexistant"}))
        self.assertFalse(self.protocole.interprete(json.dumps({"telechargerFichier":{"nom": "f2", "dossier": "d1"}})), json.dumps({"reponse": "erreurFichierLecture"}))

    #IF
    def testjson_telechargerFichierMaisDossierInexistant(self):
        self.assertTrue(self.protocole.interprete(json.dumps({"telechargerFichier":{"nom": "f2", "dossier": "d10"}})), json.dumps({"reponse": "erreurDossierInexistant"}))

    #A regarder (IF)
    def testjson_telechargerFichierMaisFichierLecture(self):
        #self.assertTrue(self.protocole.interprete(json.dumps({"telechargerFichier":{"nom": "f2", "dossier": "d1"}})), json.dumps({"reponse": "erreurFichierLecture"}))
        pass

    def testjson_supprimerFichier(self):
        self.assertTrue(self.protocole.interprete(json.dumps({"supprimerFichier":{"nom": "f2", "dossier": "d1"}})), json.dumps({"reponse": "ok"}))

    #IF
    def testjson_supprimerFichierMaisDossierInexistant(self):
        self.assertTrue(self.protocole.interprete(json.dumps({"supprimerFichier":{"nom": "f2", "dossier": "d21"}})), json.dumps({"reponse": "erreurDossierInexistant"}))

    # IF
    def testjson_supprimerFichierMaisFichierInexistant(self):
        self.assertTrue( self.protocole.interprete(json.dumps({"supprimerFichier": {"nom": "allo", "dossier": "d1"}})), json.dumps({"reponse": "erreurFichierInexistant"}))

    #A regarder (IF)
    def testjson_supprimerFichierMaisFichierLecture(self):
        #self.assertTrue(self.protocole.interprete(json.dumps({"supprimerFichier":{"nom": "f2", "dossier": "d1"}}), json.dumps({"reponse": "erreurFichierLecture"})))
        pass

    def testjson_supprimerDossier(self):
        self.assertTrue(self.protocole.interprete(json.dumps({"supprimerDossier": "d1/d2"})), json.dumps({"reponse": "ok"}))

    #IF
    def testjson_supprimerDossierMaisDossierInexistant(self):
        self.assertTrue(self.protocole.interprete(json.dumps({"supprimerDossier": "d1/d2/d3/d4/d5"})), json.dumps({"reponse": "erreurDossierInexistant"}))

    #A REGARDER (IF)
    def testjson_supprimerDossierMaisDossierLecture(self):
        #self.assertTrue(self.protocole.interprete(json.dumps({"supprimerDossier": "d1/d2"})), json.dumps({"reponse": "erreurFichierLecture"}))
        pass

    def testjson_fichierRecentOui(self):
        self.assertTrue(self.protocole.interprete(json.dumps({"questionFichierRecent":{"nom": "f1", "dossier": "d1", "date": "2016/05/20"}})), json.dumps({"reponse": "oui"}))

    def testjson_fichierRecentNon(self):
        self.assertTrue(self.protocole.interprete(json.dumps({"questionFichierRecent":{"nom": "f1", "dossier": "d1", "date": "2014/05/20"}})), json.dumps({"reponse": "non"}))

    #IF
    def testjson_fichierRecentMaisFichierInexistant(self):
        self.assertTrue(self.protocole.interprete(json.dumps({"questionFichierRecent":{"nom": "f5", "dossier": "d1", "date": "2016/05/20"}})), json.dumps({"reponse": "erreurFichierInexistant"}))

    #A REGARDER (IF)
    def testjson_fichierRecentMaisFichierLecture(self):
        #self.assertTrue(self.protocole.interprete(json.dumps({"questionFichierRecent":{"nom": "f1", "dossier": "d1", "date": "2016/05/20"}})), json.dumps({"reponse": "erreurFichierLecture"}))
        pass

    def testjson_fichierIdentiqueOui(self):
        self.assertTrue(self.protocole.interprete(json.dumps({"questionFichierIdentique":{"nom": "a1", "dossier": "b2", "signature": "c3", "date":"2016/04/19"}})), json.dumps({"reponse": "oui"}))

    def testjson_fichierIdentiqueNon(self):
        self.assertTrue(self.protocole.interprete(json.dumps({"questionFichierIdentique": {"nom": "a1", "dossier": "b2", "signature": "c4", "date": "2016/04/19"}})), json.dumps({"reponse": "non"}))

    def testjson_quitter(self):
        self.assertTrue(self.protocole.interprete(json.dumps({"action": "quitter"})), json.dumps({"reponse": "bye"}))