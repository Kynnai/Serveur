from unittest import TestCase
from serveur.protocoleXml import ProtocoleXml

class TestProtocole_xml(TestCase):
    PREFIXE_XML = "<?xml version=\"1.0\" ?>"
    nom = "a1"
    dossier = "b2"
    dossiers = "d1/d2/d3/"
    fichiers = "d1"
    signature = "c3"
    contenu = "d4"
    date = "2016/04/19"

    def setUp(self):
        self.protocole = ProtocoleXml()


    def testXml_bonjour(self):
        self.assertTrue(self.protocole.interprete('<bonjourServeur />'), self.PREFIXE_XML + '<bonjourClient />')

    def testXml_questionNomServeur(self):
        self.assertTrue(self.protocole.interprete('<questionNomServeur />'), self.PREFIXE_XML + '<nomServeur>Ubuntu Dropbox 1.0</nomServeur>')

    def testXml_listeDossier(self):
        self.assertTrue(self.protocole.interprete('<questionListeDossiers>d1</questionListeDossiers>'), self.PREFIXE_XML + '<listeDossiers><dossier>d1/d2</dossier></listeDossiers>')

    # IF
    def testXml_listeDossierInexistant(self):
        self.assertTrue(self.protocole.interprete('<questionListeDossiers>d20</questionListeDossiers>'), self.PREFIXE_XML + '<erreurDossierInexistant/>')

    # A regarder (IF)
    def testXml_listeDossierEnLecture(self):
        self.assertTrue(self.protocole.interprete('<questionListeDossiers>d1</questionListeDossiers>'), self.PREFIXE_XML + '<erreurDossierLecture/>')

    def testXml_listeFichiers(self):
        self.assertTrue(self.protocole.interprete('<questionListeFichiers>d1</questionListeFichiers>'), self.PREFIXE_XML + '<listeFichiers><fichier>d1/f1</fichier></listeFichiers/>')

    # IF
    def testXml_listeFichiersMaisDossierInexistant(self):
        self.assertTrue(self.protocole.interprete('<questionListeFichiers>d20</questionListeFichiers>'), self.PREFIXE_XML + '<erreurDossierInexistant/>')

    # A REGARDER (IF)
    def testXml_listeFichiersMaisDossierLecture(self):
        self.assertTrue(self.protocole.interprete('<questionListeFichiers>d1</questionListeFichiers>'), self.PREFIXE_XML + '<erreurDossierLecture/>')

    def testXml_creerDossier(self):
        self.assertTrue(self.protocole.interprete('<creerDossier>d7/d8/d10</creerDossier>'), self.PREFIXE_XML + '<ok />')

    # IF
    def testXml_creerDossierDejaExistant(self):
        self.assertTrue(self.protocole.interprete('<creerDossier>d1</creerDossier>'), self.PREFIXE_XML + '<erreurDossierExiste/>')

    # IF
    def testXml_creerDossierDansRepertoirNonExistant(self):
        self.assertTrue(self.protocole.interprete('<creerDossier>d10/d11</creerDossier>'), self.PREFIXE_XML + '<erreurDossierInexistant/>')

    def testXml_televerserFichier(self):
        self.assertTrue(self.protocole.interprete(
            '<televerserFichier><nom>' + self.nom + '</nom><dossier>' + self.dossier + '</dossier><signature>' + self.signature + '</signature><contenu>' + self.contenu + '</contenu)<date>' + self.date + '</date></televerserFichier>'),
            self.PREFIXE_XML + '<ok />')

    # IF
    def testXml_televerserFichierFichierDejaExistant(self):
        pass

    def testXml_telechargerFichier(self):
        self.assertTrue(self.protocole.interprete(
            '<telechargerFichier><nom>' + self.nom + '</nom><dossier>' + self.dossier + '</dossier></telechargerDossier>'),
            self.PREFIXE_XML + '<fichier><signature>' + self.signature + '</signature><contenu>' + self.contenu + '</contenu><date>' + self.date + '</date></fichier>')

    # IF
    def testXml_telechargerFichierMaisDossierInexistant(self):
        self.assertTrue(self.protocole.interprete(
            '<telechargerFichier><nom>' + self.nom + '</nom><dossier>d20</dossier></telechargerDossier>'),
            self.PREFIXE_XML + '<erreurFichierInexistant/>')

    # A regarder (IF)
    def testXml_telechargerFichierMaisFichierLecture(self):
        pass

    def testXml_supprimerFichier(self):
        self.assertTrue(self.protocole.interprete('<supprimerFichier><nom>' + self.nom + '</nom><dossier>' + self.dossier + '</dossier></supprimerFichier>'), self.PREFIXE_XML + '<ok/>')

    # IF
    def testXml_supprimerFichierMaisDossierInexistant(self):
        self.assertTrue(self.protocole.interprete('<supprimerFichier><nom>' + self.nom + '</nom><dossier>d20</dossier></supprimerFichier>'), self.PREFIXE_XML + '<erreurDossierInexistant/>')

    # IF
    def testXml_supprimerFichierMaisFichierInexistant(self):
        self.assertTrue(self.protocole.interprete('<supprimerFichier><nom>Allo</nom><dossier>' + self.dossier + '</dossier></supprimerFichier>'), self.PREFIXE_XML + '<erreurFichierInexistant/>')

    # A regarder (IF)
    def testXml_supprimerFichierMaisFichierLecture(self):
        pass

    def testXml_supprimerDossier(self):
        self.assertTrue(self.protocole.interprete('<supprimerDossier>' + self.dossiers + '</supprimerDossier>'), self.PREFIXE_XML + '<ok/>')

    # IF
    def testXml_supprimerDossierMaisDossierInexistant(self):
        self.assertTrue(self.protocole.interprete('<supprimerDossier>d1/d10/d25</supprimerDossier>'), self.PREFIXE_XML + '<erreurDossierInexistant/>')

    # A REGARDER (IF)
    def testXml_supprimerDossierMaisDossierLecture(self):
        pass

    def testXml_fichierRecentOui(self):
        self.assertTrue(self.protocole.interprete('<questionFichierRecent><nom>' + self.nom + '</nom><dossier>' + self.dossier + '</dossier><date>' + self.date + '</date></questionFichierRecent>'), self.PREFIXE_XML + '<oui/>')

    def testXml_fichierRecentNon(self):
        self.assertTrue(self.protocole.interprete('<questionFichierRecent><nom>' + self.nom + '</nom><dossier>' + self.dossier + '</dossier><date>' + "2016/03/19" + '</date></questionFichierRecent>'), self.PREFIXE_XML + '<non/>')

    # IF
    def testXml_fichierRecentMaisFichierInexistant(self):
        self.assertTrue(self.protocole.interprete('<questionFichierRecent><nom>Allo</nom><dossier>' + self.dossier + '</dossier><date>' + "2016/03/19" + '</date></questionFichierRecent>'), self.PREFIXE_XML + '<erreurFichierInexistant/>')

    # A REGARDER (IF)
    def testXml_fichierRecentMaisFichierLecture(self):
        pass

    def testXml_fichierIdentiqueOui(self):
        self.assertTrue(self.protocole.interprete(
            '<questionFichierIdentique><nom>' + self.nom + '</nom><dossier>' + self.dossier + '</dossier><signature>' + self.signature + '</signature><date>' + self.date + '</date></questionFichierIdentique>'),
            self.PREFIXE_XML + '<oui/>')

    def testXml_fichierIdentiqueNon(self):
        self.assertTrue(self.protocole.interprete(
            '<questionFichierIdentique><nom>' + self.nom + '</nom><dossier>' + self.dossier + '</dossier><signature>' + self.signature + '</signature><date>' + "2016/03/15" + '</date></questionFichierIdentique>'),
            self.PREFIXE_XML + '<non/>')

    def testXml_quitter(self):
       self.assertTrue(self.protocole.interprete('<quitter/>'), '<bye/>')