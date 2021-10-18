import RPi.GPIO as GPIO
import time
from signal import signal, SIGTERM, SIGHUP, pause
from rpi_lcd import LCD
import MAX6675 as MAX6675
import pygame
import time
import socket
import gpiozero

lcd = LCD()

#encouder declaration
clk = 22                                                                                                                                                                                                                                                                                                                                                
dt = 27
button1= 17
buttonSt = 0
counter = 0
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(clk, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(dt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(button1,GPIO.IN,pull_up_down=GPIO.PUD_UP)

volum = 0
#THERMOCOUPLE declaration
CLK = 24
CS  = 23
DO1  = 25
units = "c"
thermocouple1 = MAX6675.MAX6675(CLK, CS, DO1, units)
 
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
#lcd fonction
def safe_exit(signum, frame):
    exit(1)

signal(SIGTERM, safe_exit)
signal(SIGHUP, safe_exit)

lcd.text("Raspberry Pi ", 1)
lcd.text("menu test", 2)
time.sleep(1.5)
lcd.text("ready",1)
#music declaration
pygame.mixer.init()
pygame.display.init()

screen = pygame.display.set_mode ( ( 420 , 240 ) )

#encoder bouton fonction
def boutton_pos() :
    global buttonSt
        
    if GPIO.input(button1) == 0 :
            buttonSt = 1
            #time.sleep(0.5)
    else :
        buttonSt = 0

#encoder counter fonction
def counter_pos(first, last ):
    global counter
    
    if GPIO.input(clk) == 1 and GPIO.input(dt) == 0:
        counter = counter + 1
        time.sleep(0.01) 
    if counter >= last :
        counter = last
                    
    if GPIO.input(clk) == 0 and GPIO.input(dt) == 1:
        counter = counter - 1
        time.sleep(0.01)
    if counter <= first :
        counter = first
        
    return counter

#volum up/down fonction 
def volum_level(first , last):
    global volum
    
    if GPIO.input(clk) == 1 and GPIO.input(dt) == 0:
        volum = volum + 0.1
        time.sleep(0.01) 
    if volum >= last :
        volum = last
                    
    if GPIO.input(clk) == 0 and GPIO.input(dt) == 1:
        volum = volum - 0.1
        time.sleep(0.01)
    if volum <= first :
        volum = first
        
    return volum    

#ip address fonction   
def get_ip_address():
 ip_address = '';
 s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
 s.connect(("8.8.8.8",80))
 ip_address = s.getsockname()[0]
 s.close()
 return ip_address

#relay fonction
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
def relay_menu():
    while True :
                counter_pos(1, 10)
                boutton_pos()
                lcd.text(" R1  R2  R3  R4 '", 1)
                lcd.text(" R5  R6  R7  R8 '", 2)
                if counter_pos(1, 10) == 1 :
                    lcd.text(">    R2  R3  R4 '", 1)
                    lcd.text(" R5  R6  R7  R8 '", 2)
                if counter_pos(1, 10) == 2 :
                    lcd.text(" R1 >    R3  R4 '", 1)
                    lcd.text(" R5  R6  R7  R8 '", 2)
                if counter_pos(1, 10) == 3 :
                    lcd.text(" R1  R2 >    R4 '", 1)
                    lcd.text(" R5  R6  R7  R8 '", 2)
                if counter_pos(1, 10) == 4 :
                    lcd.text(" R1  R2  R3 >   '", 1)
                    lcd.text(" R5  R6  R7  R8 '", 2)
                if counter_pos(1, 10) == 5 :
                    lcd.text(" R1  R2  R3  R4> ", 1)
                    lcd.text(" R5  R6  R7  R8 '", 2)
                if counter_pos(1, 10) == 6 :
                    lcd.text(" R1  R2  R3  R4 '", 1)
                    lcd.text(">    R6  R7  R8 '", 2)
                if counter_pos(1, 10) == 7 :
                    lcd.text(" R1  R2  R3  R4 '", 1)
                    lcd.text(" R5 >    R7  R8 '", 2)
                if counter_pos(1, 10) == 8 :
                    lcd.text(" R1  R2  R3  R4 '", 1)
                    lcd.text(" R5  R6 >    R8 '", 2)
                if counter_pos(1, 10) == 9 :
                    lcd.text(" R1  R2  R3  R4 '", 1)
                    lcd.text(" R5  R6  R7 >   '", 2)
                if counter_pos(1, 10) == 10 :
                    lcd.text(" R1  R2  R3  R4 '", 1)
                    lcd.text(" R5  R6  R7  R8> ", 2)
                if buttonSt == 1 :
                    if counter_pos(1, 10) == 1 :
                        while True :
                            boutton_pos()
                            Str1 = str (St1)
                            lcd.text("RELAY1 is :" + Str1, 1)
                            lcd.text(" ON  OFF  RET", 2)
                            if counter_pos(1, 3) == 1 :
                                lcd.text("RELAY1 is :" + Str1, 1)
                                lcd.text(">    OFF  RET", 2)
                            if counter_pos(1, 3) == 2 :
                                lcd.text("RELAY1 is :" + Str1, 1)
                                lcd.text(" ON >     RET", 2)
                            if counter_pos(1, 3) == 3 :
                                lcd.text("RELAY1 is :" + Str1, 1)
                                lcd.text(" ON  OFF >   ", 2)                                       
                            if buttonSt == 1 :
                                if counter_pos(1, 3) == 1 :
                                    set_relay( 1, True)
                                if counter_pos(1, 3) == 2 :
                                    set_relay( 1, False)
                                if counter_pos(1, 3) == 3 :
                                    break
                    if counter_pos(1, 10) == 2 :
                        while True :
                            boutton_pos()
                            Str2 = str (St2)
                            lcd.text("RELAY2 is :" + Str2, 1)
                            lcd.text(" ON  OFF  RET", 2)
                            if counter_pos(1, 3) == 1 :
                                lcd.text("RELAY2 is :" + Str2, 1)
                                lcd.text(">    OFF  RET", 2)
                            if counter_pos(1, 3) == 2 :
                                lcd.text("RELAY2 is :" + Str2, 1)
                                lcd.text(" ON >     RET", 2)
                            if counter_pos(1, 3) == 3 :
                                lcd.text("RELAY2 is :" + Str2, 1)
                                lcd.text(" ON  OFF >   ", 2)                                       
                            if buttonSt == 1 :
                                if counter_pos(1, 3) == 1 :
                                    set_relay( 2, True)
                                if counter_pos(1, 3) == 2 :
                                    set_relay( 2, False)
                                if counter_pos(1, 3) == 3 :
                                    break
                    if counter_pos(1, 10) == 3 :
                        while True :
                            boutton_pos()
                            Str3 = str (St3)
                            lcd.text("RELAY3 is :" + Str3, 1)
                            lcd.text(" ON  OFF  RET", 2)
                            if counter_pos(1, 3) == 1 :
                                lcd.text("RELAY3 is :" + Str3, 1)
                                lcd.text(">    OFF  RET", 2)
                            if counter_pos(1, 3) == 2 :
                                lcd.text("RELAY3 is :" + Str3, 1)
                                lcd.text(" ON >     RET", 2)
                            if counter_pos(1, 3) == 3 :
                                lcd.text("RELAY3 is :" + Str3, 1)
                                lcd.text(" ON  OFF >   ", 2)                                       
                            if buttonSt == 1 :
                                if counter_pos(1, 3) == 1 :
                                    set_relay( 3, True)
                                if counter_pos(1, 3) == 2 :
                                    set_relay( 3, False)
                                if counter_pos(1, 3) == 3 :
                                    break
                    if counter_pos(1, 10) == 4 :
                        while True :
                            boutton_pos()
                            Str4 = str (St4)
                            lcd.text("RELAY4 is :" + Str4, 1)
                            lcd.text(" ON  OFF  RET", 2)
                            if counter_pos(1, 3) == 1 :
                                lcd.text("RELAY4 is :" + Str4, 1)
                                lcd.text(">    OFF  RET", 2)
                            if counter_pos(1, 3) == 2 :
                                lcd.text("RELAY4 is :" + Str4, 1)
                                lcd.text(" ON >     RET", 2)
                            if counter_pos(1, 3) == 3 :
                                lcd.text("RELAY4 is :" + Str4, 1)
                                lcd.text(" ON  OFF >   ", 2)                                       
                            if buttonSt == 1 :
                                if counter_pos(1, 3) == 1 :
                                    set_relay( 4, True)
                                if counter_pos(1, 3) == 2 :
                                    set_relay( 4, False)
                                if counter_pos(1, 3) == 3 :
                                    break
                    if counter_pos(1, 10) == 5 :
                        break
                    
                    if counter_pos(1, 10) == 6 :
                        while True :
                            boutton_pos()
                            Str5 = str (St5)
                            lcd.text("RELAY5 is :" + Str5, 1)
                            lcd.text(" ON  OFF  RET", 2)
                            if counter_pos(1, 3) == 1 :
                                lcd.text("RELAY5 is :" + Str5, 1)
                                lcd.text(">    OFF  RET", 2)
                            if counter_pos(1, 3) == 2 :
                                lcd.text("RELAY5 is :" + Str5, 1)
                                lcd.text(" ON >     RET", 2)
                            if counter_pos(1, 3) == 3 :
                                lcd.text("RELAY5 is :" + Str5, 1)
                                lcd.text(" ON  OFF >   ", 2)                                       
                            if buttonSt == 1 :
                                if counter_pos(1, 3) == 1 :
                                    set_relay( 5, True)
                                if counter_pos(1, 3) == 2 :
                                    set_relay( 5, False)
                                if counter_pos(1, 3) == 3 :
                                    break
                    if counter_pos(1, 10) == 7 :
                        while True :
                            boutton_pos()
                            Str6 = str (St6)
                            lcd.text("RELAY6 is :" + Str6, 1)
                            lcd.text(" ON  OFF  RET", 2)
                            if counter_pos(1, 3) == 1 :
                                lcd.text("RELAY6 is :" + Str6, 1)
                                lcd.text(">    OFF  RET", 2)
                            if counter_pos(1, 3) == 2 :
                                lcd.text("RELAY6 is :" + Str6, 1)
                                lcd.text(" ON >     RET", 2)
                            if counter_pos(1, 3) == 3 :
                                lcd.text("RELAY6 is :" + Str6, 1)
                                lcd.text(" ON  OFF >   ", 2)                                       
                            if buttonSt == 1 :
                                if counter_pos(1, 3) == 1 :
                                    set_relay( 6, True)
                                if counter_pos(1, 3) == 2 :
                                    set_relay( 6, False)
                                if counter_pos(1, 3) == 3 :
                                    break
                    if counter_pos(1, 10) == 8 :
                        while True :
                            boutton_pos()
                            Str7 = str (St7)
                            lcd.text("RELAY7 is :" + Str7, 1)
                            lcd.text(" ON  OFF  RET", 2)
                            if counter_pos(1, 3) == 1 :
                                lcd.text("RELAY7 is :" + Str7, 1)
                                lcd.text(">    OFF  RET", 2)
                            if counter_pos(1, 3) == 2 :
                                lcd.text("RELAY7 is :" + Str7, 1)
                                lcd.text(" ON >     RET", 2)
                            if counter_pos(1, 3) == 3 :
                                lcd.text("RELAY7 is :" + Str7, 1)
                                lcd.text(" ON  OFF >   ", 2)                                       
                            if buttonSt == 1 :
                                if counter_pos(1, 3) == 1 :
                                    set_relay( 7, True)
                                if counter_pos(1, 3) == 2 :
                                    set_relay( 7, False)
                                if counter_pos(1, 3) == 3 :
                                    break
                    if counter_pos(1, 10) == 9 :
                        while True :
                            boutton_pos()
                            Str8 = str (St8)
                            lcd.text("RELAY8 is :" + Str8, 1)
                            lcd.text(" ON  OFF  RET", 2)
                            if counter_pos(1, 3) == 1 :
                                lcd.text("RELAY8 is :" + Str8, 1)
                                lcd.text(">    OFF  RET", 2)
                            if counter_pos(1, 3) == 2 :
                                lcd.text("RELAY8 is :" + Str8, 1)
                                lcd.text(" ON >     RET", 2)
                            if counter_pos(1, 3) == 3 :
                                lcd.text("RELAY8 is :" + Str8, 1)
                                lcd.text(" ON  OFF >   ", 2)                                       
                            if buttonSt == 1 :
                                if counter_pos(1, 3) == 1 :
                                    set_relay( 8, True)
                                if counter_pos(1, 3) == 2 :
                                    set_relay( 8, False)
                                if counter_pos(1, 3) == 3 :
                                    break
                    if counter_pos(1, 10) == 10 :
                        break
def temp_menu():
    counter = 0
    print ("Counter ", counter)
    print ("botton ", buttonSt)
    while True:
        boutton_pos()
        temp1 = thermocouple1.get_temp()
        time.sleep(0.05)
        temp = str (temp1)
        lcd.text("the temp is "+temp+"C°", 1)
        lcd.text(">back", 2)
        time.sleep(0.05)
        if buttonSt == 1 :
            break
def music_menu():
                        while True:
                            boutton_pos()
                            lcd.text(" music1 ' music3", 1)
                            lcd.text(" music2 ' music4", 2)
                            if counter_pos(1,6) == 1:
                                lcd.text(">       ' music3", 1)
                                lcd.text(" music2 ' music4", 2)
                            if counter_pos(1,6) == 2:
                                lcd.text(" music1 ' music3", 1)
                                lcd.text(">       ' music4", 2)
                            if counter_pos(1,6) == 3:
                                lcd.text(" music1 '>      ", 1)
                                lcd.text(" music2 ' music4", 2)
                            if counter_pos(1,6) == 4:
                                lcd.text(" music1 ' music3", 1)
                                lcd.text(" music2 '>      ", 2)
                            if counter_pos(1,6) == 5:
                                lcd.text(" music1>  music3", 1)
                                lcd.text(" music2 ' music4", 2)
                            if counter_pos(1,6) == 6:
                                lcd.text(" music1 ' music3", 1)
                                lcd.text(" music2>  music4", 2)
                            if buttonSt == 1 :
                                if counter_pos(1,6) == 1:
                                    while True :
                                        boutton_pos()
                                        lcd.text(" play", 1)
                                        lcd.text(" stop", 2)
                                        lcd.text(">",counter_pos( 1 , 2 ))
                                        if buttonSt == 1 :
                                            if counter_pos(1,2) == 1:
                                                song1 = ( "music1.mp3" )
                                                pygame.mixer.music.load(song1)  # Get the first track from the playlist
                                                pygame.mixer.music.set_volume(volum)
                                                print ("Playing first track")
                                                pygame.mixer.music.play()
                                            if counter_pos(1,2) == 2:
                                                pygame.mixer.music.stop()
                                                break
                                                
                                if counter_pos(1,6) == 2:
                                    while True :
                                        boutton_pos()
                                        lcd.text(" play", 1)
                                        lcd.text(" stop", 2)
                                        lcd.text(">",counter_pos( 1 , 2 ))
                                        if buttonSt == 1 :
                                            if counter_pos(1,2) == 1:
                                                song1 = ( "music2.mp3" )
                                                pygame.mixer.music.load(song1)  # Get the first track from the playlist
                                                pygame.mixer.music.set_volume(volum)
                                                print ("Playing first track")
                                                pygame.mixer.music.play()
                                            if counter_pos(1,2) == 2:
                                                pygame.mixer.music.stop()
                                                break
                                            
                                if counter_pos(1,6) == 3:
                                    while True :
                                        boutton_pos()
                                        lcd.text(" play", 1)
                                        lcd.text(" stop", 2)
                                        lcd.text(">",counter_pos( 1 , 2 ))
                                        if buttonSt == 1 :
                                            if counter_pos(1,2) == 1:
                                                song1 = ( "music3.mp3" )
                                                pygame.mixer.music.load(song1)  # Get the first track from the playlist
                                                pygame.mixer.music.set_volume(volum)
                                                print ("Playing first track")
                                                pygame.mixer.music.play()
                                            if counter_pos(1,2) == 2:
                                                pygame.mixer.music.stop()
                                                break
                                            
                                if counter_pos(1,6) == 4:
                                    while True :
                                        boutton_pos()
                                        lcd.text(" play", 1)
                                        lcd.text(" stop", 2)
                                        lcd.text(">",counter_pos( 1 , 2 ))
                                        if buttonSt == 1 :
                                            if counter_pos(1,2) == 1:
                                                song1 = ( "music4.mp3" )
                                                pygame.mixer.music.load(song1)  # Get the first track from the playlist
                                                pygame.mixer.music.set_volume(volum)
                                                print ("Playing first track")
                                                pygame.mixer.music.play()
                                            if counter_pos(1,2) == 2:
                                                pygame.mixer.music.stop()
                                                break
                                                
                                if counter_pos(1,6) == 5:
                                    while True:
                                        boutton_pos()
                                        volum_level(0, 1)
                                        v = str (volum *10)
                                        lcd.text("volum : "+ v ,1)
                                        lcd.text(">return",2)
                                        if buttonSt == 1 :
                                            break
                                        
                                if counter_pos(1,6) == 6:
                                    break
    
def LCD_menu() :
    global counter
    global buttonSt
    global St1
    counter_pos( 1 , 3 )
    
    lcd.text(" relay", 1)
    lcd.text(" temp    next", 2)
    lcd.text(">",counter_pos( 1 , 3 ))
    if counter_pos( 1 , 3 ) == 3 :
        lcd.text(" temp   >next", 2)
        
    if buttonSt == 1 :
        if counter_pos( 1 , 3 ) == 1 :
                        #the relay menu
            while True :
                relay_menu()
                if counter_pos(1, 10) == 10 :
                    break

        if counter_pos( 1 , 3 ) == 2 :
                        #the temp menu
            buttonSt = 0
            while True :
                temp_menu()
                if buttonSt == 1 :
                    break
        
        
                
                        #next page
        if counter_pos( 1 , 3 ) == 3 :
            while True :
                print ("Counter ", counter)
                print ("botton ", buttonSt)
                boutton_pos()
                lcd.text(" music", 1)
                lcd.text(" wifi_st    next", 2)
                lcd.text(">",counter_pos( 1 , 3 ))
                if counter_pos( 1 , 3 ) == 3 :
                    lcd.text(" wifi_st   >next", 2)
                    if buttonSt == 1 :
                        break
                
                if buttonSt == 1 :
                                    #music menu
                    if counter_pos( 1 , 3 ) == 1 :
                        while True :
                            music_menu()
                            if counter_pos(1,6) == 6:
                                break
                    
                    if counter_pos( 1 , 3 ) == 2 :
                        while True:
                            boutton_pos()
                            lcd.text("ip:" + get_ip_address() ,1)
                            lcd.text(">back",2)
                            if buttonSt == 1 :
                                break

             
while True : 
    
    LCD_menu()
    boutton_pos()


    #temp_menu()
    print ("Counter ", counter)
    print ("botton ", buttonSt)

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

        
            
    

