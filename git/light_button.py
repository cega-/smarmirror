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
button_main_light = 17
button_snake_light = 23
button_screen_light = 24
l_pin = [button_main_light,button_snake_light,button_screen_light]                                #broche utilisé en entrée
pin_main_light = 22
pin_snake_light = 27
#temps = 1                              #valeur attente en msec
#temps = 10
#temps = 100
#temps = 100
temps = 1000
bounce = 500
l_pushed = []

def switch_main_light(channel):
 print("push {0}".format(channel))
 if channel not in l_pushed:
  l_pushed.append(channel)
  print(l_pushed)
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(pin_main_light, GPIO.OUT)
  GPIO.output(pin_main_light, GPIO.LOW)
 else :
  l_pushed.remove(channel)
  GPIO.output(pin_main_light, GPIO.HIGH)

def switch_snake_light(channel):
 print("push {0}".format(channel))
 if channel not in l_pushed:
  l_pushed.append(channel)
  print(l_pushed)
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(pin_snake_light, GPIO.OUT)
  GPIO.output(pin_snake_light, GPIO.LOW)
 else :
  l_pushed.remove(channel)
  GPIO.output(pin_snake_light, GPIO.HIGH)

def my_callback(channel):
 print("push {0}".format(channel))

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
      GPIO.add_event_detect(button_main_light, GPIO.BOTH, callback=switch_main_light, bouncetime=bounce)
      GPIO.add_event_detect(button_snake_light, GPIO.BOTH, callback=switch_snake_light, bouncetime=bounce)
      GPIO.add_event_detect(pin, GPIO.BOTH, callback=my_callback, bouncetime=bounce)
      while True:                    #boucle infinie
       #    for pin in l_pin:
        #     entree = GPIO.input(pin)   #lecture entrée
         #    if (entree == True):       #si touche appuyée
          #       print("BP appuyé {0}".format(pin))     #IHM
             time.sleep(temps / 1000)   #attente en msec 
     except KeyboardInterrupt:          #sortie boucle par ctrl-c
#         GPIO.output(pin_main_light, GPIO.HIGH)
         GPIO.cleanup()                 #libère toutes les ressources
         print("\nFin du programme\n")  #IHM
