import RPi.GPIO as GPIO
import time
from signal import signal, SIGTERM, SIGHUP, pause
from rpi_lcd import LCD
import MAX6675 as MAX6675

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

#THERMOCOUPLE declaration
CLK = 24
CS  = 23
DO1  = 25
units = "c"
thermocouple1 = MAX6675.MAX6675(CLK, CS, DO1, units)

#lcd fonction
def safe_exit(signum, frame):
    exit(1)

signal(SIGTERM, safe_exit)
signal(SIGHUP, safe_exit)

lcd.text("Raspberry Pi ", 1)
lcd.text("menu test", 2)
time.sleep(1.5)
lcd.text("ready",1)
#encoder bouton fonction
def boutton_pos() :
    global buttonSt
        
    if GPIO.input(button1) == 0 :
            buttonSt = 1
            time.sleep(0.5)
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
     
            
def principal_menu() :
    global counter
    global buttonSt
    counter_pos( 1 , 2 )
    
    lcd.text(" relay", 1)
    lcd.text(" temp", 2)
    lcd.text(">",counter_pos( 1 , 2 ))

    if buttonSt == 1 :
        if counter_pos( 1 , 2 ) == 1 :
    #the relay menu
            while True :
                counter_pos(1, 2)
                lcd.text("relay 1 : ON", 1)
                lcd.text("relay 2 : OFF", 2)            
        elif counter_pos( 1 , 2 ) == 2 :
    #the temp menu
            while True :
        
        
                counter = 0
                print ("Counter ", counter)
                print ("botton ", buttonSt)
                boutton_pos()
                temp1 = thermocouple1.get_temp()
                time.sleep(0.05)
                temp = str (temp1)
                lcd.text("the temp is "+temp+"C°", 1)
                lcd.text(">back", 2)
                time.sleep(0.05)
                if buttonSt == 1 :
                    break        
        
    

while True:
    
    principal_menu()
    boutton_pos()


    #temp_menu()
    print ("Counter ", counter)
    print ("botton ", buttonSt)
        
            
    
