import RPi.GPIO as GPIO
import time


clk = 4                                                                                                                                                                                                                                                                                                                                                
dt = 3
button1= 2
step = 1
buttonSt = 0
counter = 0
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(clk, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(dt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(button1,GPIO.IN,pull_up_down=GPIO.PUD_UP)
counter = 0

LCD_RS = 7
LCD_E  = 8
LCD_D4 = 25
LCD_D5 = 24
LCD_D6 = 23
LCD_D7 = 18
# Use BCM GPIO numbers
GPIO.setup(LCD_E, GPIO.OUT)  # E
GPIO.setup(LCD_RS, GPIO.OUT) # RS
GPIO.setup(LCD_D4, GPIO.OUT) # DB4
GPIO.setup(LCD_D5, GPIO.OUT) # DB5
GPIO.setup(LCD_D6, GPIO.OUT) # DB6
GPIO.setup(LCD_D7, GPIO.OUT) # DB7

# Define some device constants
LCD_WIDTH = 16    # Maximum characters per line
LCD_CHR = True
LCD_CMD = False
 
LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0# LCD RAM address for the 2nd line
 
# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005
# Counter variable



def lcd_init():
  # Initialise display
  lcd_byte(0x33,LCD_CMD) # 110011 Initialise
  lcd_byte(0x32,LCD_CMD) # 110010 Initialise
  lcd_byte(0x06,LCD_CMD) # 000110 Cursor move direction
  lcd_byte(0x0C,LCD_CMD) # 001100 Display On,Cursor Off, Blink Off
  lcd_byte(0x28,LCD_CMD) # 101000 Data length, number of lines, font size
  lcd_byte(0x01,LCD_CMD) # 000001 Clear display
  time.sleep(E_DELAY)
 
def lcd_byte(bits, mode):
  # Send byte to data pins
  # bits = data
  # mode = True  for character
  #        False for command
 
  GPIO.output(LCD_RS, mode) # RS
 
  # High bits
  GPIO.output(LCD_D4, False)
  GPIO.output(LCD_D5, False)
  GPIO.output(LCD_D6, False)
  GPIO.output(LCD_D7, False)
  if bits&0x10==0x10:
    GPIO.output(LCD_D4, True)
  if bits&0x20==0x20:
    GPIO.output(LCD_D5, True)
  if bits&0x40==0x40:
    GPIO.output(LCD_D6, True)
  if bits&0x80==0x80:
    GPIO.output(LCD_D7, True)
 
  # Toggle 'Enable' pin
  lcd_toggle_enable()
 
  # Low bits
  GPIO.output(LCD_D4, False)
  GPIO.output(LCD_D5, False)
  GPIO.output(LCD_D6, False)
  GPIO.output(LCD_D7, False)
  if bits&0x01==0x01:
    GPIO.output(LCD_D4, True)
  if bits&0x02==0x02:
    GPIO.output(LCD_D5, True)
  if bits&0x04==0x04:
    GPIO.output(LCD_D6, True)
  if bits&0x08==0x08:
    GPIO.output(LCD_D7, True)
 
  # Toggle 'Enable' pin
  lcd_toggle_enable()
 
def lcd_toggle_enable():
  # Toggle enable
  time.sleep(E_DELAY)
  GPIO.output(LCD_E, True)
  time.sleep(E_PULSE)
  GPIO.output(LCD_E, False)
  time.sleep(E_DELAY)
 
def lcd_string(message,line):
  # Send string to display
 
  message = message.ljust(LCD_WIDTH," ")
 
  lcd_byte(line, LCD_CMD)
 
  for i in range(LCD_WIDTH):
    lcd_byte(ord(message[i]),LCD_CHR)
    

lcd_init()
lcd_string("Rasbperry Pi",LCD_LINE_1)
lcd_string("menu Test",LCD_LINE_2)
time.sleep(2)
lcd_string("      ",LCD_LINE_1)
lcd_string("READY!",LCD_LINE_2)
time.sleep(0.1)
    
def boutton_pos() :
    global buttonSt
        
    if GPIO.input(button1) == 0 :
            buttonSt = 1
            time.sleep(0.5)
    else :
        buttonSt = 0
            
def counter_pos(first ,last):
    global counter
    
    if GPIO.input(clk) == 1 and GPIO.input(dt) == 0:
        counter = counter + 1
        time.sleep(0.5)
       
        if counter >= last :
            counter = last
         
    if GPIO.input(clk) == 0 and GPIO.input(dt) == 1:
        counter = counter - 1
        time.sleep(0.5)
        
        if counter <= first :
            counter = first
            
def principal_menu() :
    
    lcd_string("1 relay ",LCD_LINE_1)
    lcd_string("2 temp",LCD_LINE_2)
            
        
    while True:
        print("counter :",counter)
        print("bouton :",buttonSt)
        n = counter_pos(0,1)
        if buttonSt == 1:

            
    
        
def temp_menu()  :
    
    global counter
    global buttonSt
    
    
    counter_pos(2,3)
    if counter == 2 :
        lcd_string("the temp is:",LCD_LINE_1)
        lcd_string("40 C°    back",LCD_LINE_2)
        time.sleep(0.05)
    if counter == 3 :
        lcd_string("the temp is:",LCD_LINE_1)
        lcd_string("40 C°   >back",LCD_LINE_2)
        time.sleep(0.05)

def relay_menu() :

        lcd_string("relay 1 : ON",LCD_LINE_1)
        lcd_string("relay 2 : OFF",LCD_LINE_2)
        
    

while True:
    
    principal_menu()
    boutton_pos()

    #temp_menu()
    print ("Counter ", counter)
    print ("botton ", buttonSt)
        
            
    