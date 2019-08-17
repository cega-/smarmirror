#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
Programme classique lecture entrée GPIO avec la bibliothèque RPi.GPIO
utilisation de la fonction GPIO.input()
Bouton poussoir raccordé entre GPIO22 et +3.3V 
(avec résistance de protection de 1k en série)
nom programme       : push01.py
logiciel            : python 3.4.2
cible               : raspberry Pi
date de création    : 18/08/2016
date de mise à jour : 18/08/2016
version             : 1.0
auteur              : icarePetibles
référence           : 
"""
#-------------------------------------------------------------------------------
# Bibliothèques
#-------------------------------------------------------------------------------
import RPi.GPIO as GPIO                 #bibliothèque RPi.GPIO
import time                             #bibliothèque time
#-------------------------------------------------------------------------------
l_pin = [17,23,24]                                #broche utilisé en entrée
#temps = 1                              #valeur attente en msec
#temps = 10
temps = 100
#temps = 100
#temps = 1000
 
GPIO.setwarnings(False)                 #désactive le mode warning
GPIO.setmode(GPIO.BCM)                  #utilisation des numéros de ports du
                                        #processeur
for pin in l_pin:
 GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
                                        #mise en entrée du port GPIO 22
                                        #et activation résistance soutirage
                                        #au ground
if __name__ == '__main__':
     """
     Programme par défaut
     """
     print("Début du programme")        #IHM
     print("Sortie par ctrl-c\n")       #IHM
     try:
         while True:                    #boucle infinie
           for pin in l_pin:
             entree = GPIO.input(pin)   #lecture entrée
             if (entree == True):       #si touche appuyée
                 print("BP appuyé {0}".format(pin))     #IHM
             time.sleep(temps / 1000)   #attente en msec 
     except KeyboardInterrupt:          #sortie boucle par ctrl-c
         GPIO.cleanup()                 #libère toutes les ressources
         print("\nFin du programme\n")  #IHM
