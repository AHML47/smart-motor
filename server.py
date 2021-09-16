from http.server import BaseHTTPRequestHandler, HTTPServer
import subprocess
import socket
import pygame
import time
import gpiozero

Reuqest = None

#music declaration
pygame.mixer.init()
pygame.display.init()



song1 = "music1.mp3"
song2 = "music2.mp3"
song3 = "music3.mp3"

#relay declaration
RELAY_PIN1 = 26
RELAY_PIN2 = 19
RELAY_PIN3 = 13
RELAY_PIN4 =  6
RELAY_PIN5 =  5
RELAY_PIN6 =  0
RELAY_PIN7 = 11
RELAY_PIN8 =  9

relay1 = gpiozero.OutputDevice(RELAY_PIN1, active_high=False, initial_value=False)
relay2 = gpiozero.OutputDevice(RELAY_PIN2, active_high=False, initial_value=False)
relay3 = gpiozero.OutputDevice(RELAY_PIN3, active_high=False, initial_value=False)
relay4 = gpiozero.OutputDevice(RELAY_PIN4, active_high=False, initial_value=False)
relay5 = gpiozero.OutputDevice(RELAY_PIN5, active_high=False, initial_value=False)
relay6 = gpiozero.OutputDevice(RELAY_PIN6, active_high=False, initial_value=False)
relay7 = gpiozero.OutputDevice(RELAY_PIN7, active_high=False, initial_value=False)
relay8 = gpiozero.OutputDevice(RELAY_PIN8, active_high=False, initial_value=False)

PIN = 0

St1 = 0
St2 = 0
St3 = 0
St4 = 0
St5 = 0
St6 = 0
St7 = 0
St8 = 0

def get_ip_address():
 ip_address = '';
 s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
 s.connect(("8.8.8.8",80))
 ip_address = s.getsockname()[0]
 s.close()
 return ip_address

def set_relay( PIN, status):
    global St1
    global St2
    global St3
    global St4
    global St5
    global St6
    global St7
    global St8
    if PIN == 1 :
        if status:
            print("Setting relay1: ON")
            relay1.on()
            St1 = 1
        else:
            print("Setting relay1: OFF")
            relay1.off()
            St1 = 0
    if PIN == 2 :
        if status:
            print("Setting relay2: ON")
            relay2.on()
            St2 = 1
        else:
            print("Setting relay2: OFF")
            relay2.off()
            St2 = 0
    if PIN == 3 :
        if status:
            print("Setting relay3: ON")
            relay3.on()
            St3 = 1
        else:
            print("Setting relay3: OFF")
            relay3.off()
            St3 = 0
    if PIN == 4 :
        if status:
            print("Setting relay4: ON")
            relay4.on()
            St4 = 1
        else:
            print("Setting relay4: OFF")
            relay4.off()
            St4 = 0
    if PIN == 5 :
        if status:
            print("Setting relay5: ON")
            relay5.on()
            St5 = 1
        else:
            print("Setting relay5: OFF")
            relay5.off()
            St5 = 0
    if PIN == 6 :
        if status:
            print("Setting relay6: ON")
            relay6.on()
            St6 = 1
        else:
            print("Setting relay6: OFF")
            relay6.off()
            St6 = 0
    if PIN == 7 :
        if status:
            print("Setting relay7: ON")
            relay7.on()
            St7 = 1
        else:
            print("Setting relay7: OFF")
            relay7.off()
            St7 = 0
    if PIN == 8 :
        if status:
            print("Setting relay8: ON")
            relay8.on()
            St8 = 1
        else:
            print("Setting relay8: OFF")
            relay8.off()
            St8 = 0
    return St1,St2,St3,St4,St5,St6,St7,St8

class RequestHandler_httpd(BaseHTTPRequestHandler):
  def do_GET(self):
    global Reuqest
    messagetosend = bytes('HELLO WORLD',"utf")
    self.send_response(200)
    self.send_header('Content-Type', 'text/plain')
    self.send_header('Content-Length', len(messagetosend))
    self.end_headers()
    self.wfile.write(messagetosend)
    Reuqest = self.requestline
    Reuqest = Reuqest[5 : int(len(Reuqest)-9)]
    print(Reuqest)

    if Reuqest == 'S1':
      pygame.mixer.music.load( "music1.mp3" )  # Get the first track from the playlist
      pygame.mixer.music.set_volume(0.1)
      print ("Playing first track")
      pygame.mixer.music.play()
      
    if Reuqest == 'S2':
      pygame.mixer.music.load(song2)  # Get the first track from the playlis
      pygame.mixer.music.set_volume(0.1)
      print ("Playing first track")
      pygame.mixer.music.play()
      
    if Reuqest == 'S3':
      pygame.mixer.music.load(song3)  # Get the first track from the playlis
      pygame.mixer.music.set_volume(0.1)
      print ("Playing first track")
      pygame.mixer.music.play()
      
    if Reuqest == 'STOP' :
        pygame.mixer.music.stop()

    
    #dhaw godami
    if Reuqest == 'L1O':
        set_relay( 1, True )
    if Reuqest == 'L1F':
        set_relay( 1, False)
    
    #cliniton imin
    if Reuqest == 'LRO':
        set_relay( 2,True)
    if Reuqest == 'LRF':
        set_relay( 2,False)
        
    #cliniton isar
    if Reuqest == 'LLO':
        set_relay( 3,True)
    if Reuqest == 'LLF':
        set_relay( 3,False)
    
    #ta5tif
    if Reuqest == 'OM':
        set_relay( 4,True)
        set_relay( 5,True)
    if Reuqest == 'CM':
        set_relay( 4,False)
        set_relay( 5,False)
    return Reuqest
    


server_address_httpd = (get_ip_address(),8080)
httpd = HTTPServer(server_address_httpd, RequestHandler_httpd)
print('starting server')
httpd.serve_forever()

running = True
while running:
   for event in pygame.event.get():
      if event.type == pygame.USEREVENT:    # A track has ended
         print ("Track has ended")
         if playlist:       # If there are more tracks in the queue... (A non-empty list is True)
            print ("Songs left in playlist@ {}".format(len(playlist)))
            song = playlist.pop()
            print ("Queuing next song: {}".format(song))
            pygame.mixer.music.queue ( song ) # Queue the next one in the list
         else:
            print ("Playlist is empty")

