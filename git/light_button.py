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
button_snake_light = 24
button_screen_light = 23
l_pin = [button_main_light,button_snake_light,button_screen_light]                                #broche utilisé en entrée
pin_main_light = 27
pin_snake_light = 22
#temps = 1                              #valeur attente en msec
#temps = 10
temps = 50
#temps = 100
#temps = 1000
bounce = 500
l_pushed = []

def switch_main_light():
 if not gpioRead2[pin]['switch']:
  gpioRead2[pin]['switch'] = True
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(pin_main_light, GPIO.OUT)
  GPIO.output(pin_main_light, GPIO.LOW)
  print('Switch ON Main')
 else :
  gpioRead2[pin]['switch'] = False
  GPIO.output(pin_main_light, GPIO.HIGH)

def switch_snake_light():
 if not gpioRead2[pin]['switch']:
  gpioRead2[pin]['switch'] = True
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(pin_snake_light, GPIO.OUT)
  GPIO.output(pin_snake_light, GPIO.LOW)
  print('Switch ON Snake')
 else :
  gpioRead2[pin]['switch'] = False
  GPIO.output(pin_snake_light, GPIO.HIGH)

#def switch_snake_light(channel):
# print("push {0}".format(channel))
# if channel not in l_pushed:
#  l_pushed.append(channel)
#  print(l_pushed)
#  GPIO.setmode(GPIO.BCM)
#  GPIO.setup(pin_snake_light, GPIO.OUT)
#  GPIO.output(pin_snake_light, GPIO.LOW)
# else :
#  l_pushed.remove(channel)
#  GPIO.output(pin_snake_light, GPIO.HIGH)

def switch_screen_light():
 print("push {0}".format('switch_screen_light'))

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
     init_time = time.time()*1000
     gpioRead2 = {button_main_light: {'state': None, 'time': init_time, 'func': switch_main_light, 'switch': False}, button_snake_light: {'state': None, 'time': init_time, 'func': switch_snake_light, 'switch': False}, button_screen_light: {'state': None, 'time': init_time, 'func': switch_screen_light, 'switch': False}}
     control_flag_timelaps = True
     print("Début du programme")        #IHM
     print("Sortie par ctrl-c\n")       #IHM
     try:
#      GPIO.add_event_detect(button_main_light, GPIO.BOTH, callback=switch_main_light, bouncetime=bounce)
#      GPIO.add_event_detect(button_snake_light, GPIO.BOTH, callback=switch_snake_light, bouncetime=bounce)
#      GPIO.add_event_detect(pin, GPIO.BOTH, callback=my_callback, bouncetime=bounce)
      while True:                    #boucle infinie
           for pin in l_pin:
             entree = GPIO.input(pin)   #lecture entrée
             #print("{0}, {1}".format(pin, entree))
             if (entree == True):
              if (pin in gpioRead2.keys()):
               if (gpioRead2[pin]['state'] == True):
                print('reset')
                gpioRead2[pin]['state'] = False
               if (time.time()*1000 - gpioRead2[pin]['time'] > 500):
                control_flag_timelaps = True
               else:
                control_flag_timelaps = False
              else:
               control_flag_timelaps = True

              if (control_flag_timelaps):
               time.sleep( 100 / 1000 )
               gpioRead2[pin]['state'] = GPIO.input( pin )
               gpioRead2[pin]['time'] = time.time()*1000
              if (entree == gpioRead2[pin]['state']):       #si touche appuyée
                  print("BP appuyé {0}, Time {1}, Timelaps {2}".format(pin, gpioRead2[pin]['time'], time.time()*1000 - gpioRead2[pin]['time']))     #IHM
                  gpioRead2[pin]['func']()
              #time.sleep(temps / 1000)   #attente en msec 
     except KeyboardInterrupt:          #sortie boucle par ctrl-c
#         GPIO.output(pin_main_light, GPIO.HIGH)
         GPIO.cleanup()                 #libère toutes les ressources
         print("\nFin du programme\n")  #IHM
