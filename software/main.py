 
from machine import I2C, Pin
import time
import network 
import neopixel 
import gc
import bitmapfont
from font3x8 import *
from week7x7  import * 
import rx8111

import config

ssid = config.ssid
password =config.password

zonetime = 8*3600

NEOPIXEL_PIN = 5
ROWS = 8
COLS = 15
NUMBER_PIXELS = ROWS * COLS

C_BLACK=(0,0,0)
C_GREEN=(0,35,0)
C_BLUE=(0,0,35)
C_RED=(35,0,0)
C_YELLOW=(35,35,0)   
C_MONTH=(31,5,12) 
C_DAY=(35,31,31) 

np = neopixel.NeoPixel(Pin(NEOPIXEL_PIN), NUMBER_PIXELS)




#15x8
ICON_WIFI=(
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
    1,0,1,0,0,1,0,0,1,1,1,0,0,1,0,
    1,0,1,0,0,0,0,0,1,0,0,0,0,0,0,
    1,0,1,0,0,1,0,0,1,1,0,0,0,1,0,
    1,0,1,0,0,1,0,0,1,0,0,0,0,1,0,
    1,1,1,0,0,1,0,0,1,0,0,0,0,1,0,
    1,1,1,0,0,1,0,0,1,0,0,0,0,1,0,
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,

)
 
class Display(object):
    def __init__(self,np):
        self.np=np

    
    def write_pixel(self,x,y,value):
        if y >= 0 and y < ROWS and x >=0 and x < COLS:
            self.np[x*ROWS + y] = value

    def drawPixel(self,x,y,value):
        self.write_pixel(x,y,value)

        
            
    def clear(self):
        for i in range(NUMBER_PIXELS):
            np[i]=(0,0,0)            
        self.np.write()
    
    def show(self):
        self.np.write()

    def draw1Num(self,x,y,num,color,bg=None):
        num=num%10
        for j in range(8):
            for i in range(3):
                if  FONT3X8[num][i+j*3]==1:
                    self.write_pixel(x+i,y+j,color)
                else :
                    if bg != None:
                        self.write_pixel(x+i,y+j,bg)
                    
    def drawNum(self,x,y,num,color,bg=None)  :
        self.draw1Num(x,y,num//1000%10,color,bg)
        self.draw1Num(x+4,y,num%1000//100,color,bg)
        self.draw1Num(x+4*2,y,num%100//10,color,bg)
        self.draw1Num(x+4*3,y,num%10,color,bg)
        
    def change1Num(self,x,y,num_src,num_dest,color,bg=None):
        num_src=num_src%10
        num_dest=num_dest%10
        
        for i in range(1,9):
            self.draw1Num(x,y-i,num_src,color,bg)
            self.draw1Num(x,y+8-i,num_dest,color,bg)
            time.sleep(0.01)
            self.show()
    
    def draw1Week(self,x,y,num,color,bg=None):   
        for j in range(8):
            for i in range(7):
                if  WEEK7X8[num][i+j*7]==1:
                    self.write_pixel(x+i,y+j,color)
                else :
                    if bg != None:
                        self.write_pixel(x+i,y+j,bg)
    
    def drawWeek(self,x,y,watch,color,bg=None)  :
        # num=num%7
        # print(num)
        self.draw1Week(x,y,7,color,bg)
        self.draw1Week(x+8,y,watch.time_now[6],color,bg) 
    
    def drawTime(self,x,y,watch,color1,color2,bg=None): 
        self.draw1Num(x+0,y,watch.time_now[3]//10,color1,bg)
        self.draw1Num(x+4,y,watch.time_now[3]%10,color1,bg)
        self.draw1Num(x+8,y,watch.time_now[4]//10,color2,bg)
        self.draw1Num(x+12,y,watch.time_now[4]%10,color2,bg)
        self.show()
    
    def drawDate(self,x,y,watch,color1,color2,bg=None):
        if  watch.time_now[1]//10:
            self.draw1Num(x+0,y,watch.time_now[1]//10,color1,bg)
        else:
            self.draw1Num(x+0,y,watch.time_now[1]//10,bg,bg)

        self.draw1Num(x+4,y,watch.time_now[1]%10,color1,bg)
        if  watch.time_now[2]//10:            
            self.draw1Num(x+8,y,watch.time_now[2]//10,color2,bg)
        else:
            self.draw1Num(x+8,y,watch.time_now[2]//10,bg,bg)
        self.draw1Num(x+12,y,watch.time_now[2]%10,color2,bg)
        self.show()
    
    def drawIcon(self,x,y,width,height,icon,color,bg=None):
        for j in range(height):
            for i in range(width):
                if  icon[i+j*width]==1:
                    self.write_pixel(x+i,y+j,color)
                else :
                    if bg != None:
                        self.write_pixel(x+i,y+j,bg)




disp = Display(np)

import machine
class Watch(object):
    def __init__(self,time_now):
        self.time_now=time_now
        self.time_old=time_now
        self.timeout=0 #关机超时时间，ms单位
        self.timeout_stamp=time.ticks_ms()
        

    def resetTimeout(self,timeout=5000):
        self.timeout= timeout
        self.timeout_stamp=time.ticks_ms()

    def checkTimeout(self): 
        deadline = time.ticks_add(self.timeout_stamp,  self.timeout)
        if time.ticks_diff(deadline, time.ticks_ms()) > 0:
            return False
        else:
             return True


    

     

    def poweroff(self):
        machine.deepsleep()


    


INDEX_HOUR = 3
INDEX_MINUTE = 4
INDEX_SECOND = 5

 

def updateTime(watch):
    watch.time_now = rtc.datetime()
    if watch.time_now != watch.time_old:
        if watch.time_now[INDEX_MINUTE]%10 != watch.time_old[INDEX_MINUTE]%10:
            disp.change1Num(12,0,watch.time_old[INDEX_MINUTE]%10,watch.time_now[INDEX_MINUTE]%10,C_YELLOW,C_BLACK)
            
        if watch.time_now[INDEX_MINUTE]//10 != watch.time_old[INDEX_MINUTE]//10:
            disp.change1Num(8,0,watch.time_old[INDEX_MINUTE]//10,watch.time_now[INDEX_MINUTE]//10,C_YELLOW,C_BLACK)
            
        if watch.time_now[INDEX_HOUR]%10 != watch.time_old[INDEX_HOUR]%10:
            disp.change1Num(4,0,watch.time_old[INDEX_HOUR]%10,watch.time_now[INDEX_HOUR]%10,C_GREEN,C_BLACK)
            
        if watch.time_now[INDEX_HOUR]//10 != watch.time_old[INDEX_HOUR]//10:
            disp.change1Num(0,0,watch.time_old[INDEX_HOUR]//10,watch.time_now[INDEX_HOUR]//10,C_GREEN,C_BLACK)
        
        watch.time_old = watch.time_now


print('rx8111 test')
i2c = I2C(0, scl=Pin(7), sda=Pin(8), freq=400000)
rtc = rx8111.RX8111(i2c)

week=('SUN','MON','TUE','WED','THU','FRI','SAT')
 


def syncTimeByWifi(ssid,password,trycnt=20):
    if ssid == None :
        return
    import ntptime
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid,password)
    
    if not wlan.isconnected():
        while not wlan.isconnected():
            print("Waiting to connect:")
            time.sleep(1.0)
            trycnt = trycnt-1
            if trycnt%2 :
                disp.drawPixel(5,1,C_GREEN)
            else:
                disp.drawPixel(5,1,C_RED)

            disp.show()
            if trycnt<0:
                print("\nFail !!!\n")
                break
    if wlan.isconnected():     
        print(wlan.ifconfig())
        while True:
            try:
                print('获取时间中')
                ntptime.host = 'ntp1.aliyun.com'
                ntptime.settime()
                print('成功获取')
                break
            except:
                print('获取失败')
                time.sleep(1)
    wlan.disconnect()
    wlan.active(False)
    watch.resetTimeout()



charge = Pin(20, Pin.IN, Pin.PULL_UP)

k1 = Pin(4, Pin.IN)
k2 = Pin(0, Pin.IN)
k3 = Pin(9, Pin.IN)


class Event():
    K1_PRESSED=1
    K1_RELEASED=2
    K2_PRESSED=3
    K2_RELEASED=4
    K3_PRESSED=5
    K3_RELEASED=6
    K1_LONG=7
    K2_LONG=8
    K3_LONG=9

    def __init__(self):
        self.event=[]
    
    def addEvent(self,evt):
        self.event.append(evt)
    
    def getEvent(self):  
        if len(self.event)==0:
            return -1              
        return self.event.pop(0)

LongPressed = 1000       
key_time=0
def fun(key):
    global key_time
    watch.resetTimeout()
    if key==k1:
        if key.value() == 0:
            key_time=time.ticks_ms()
            # print('k1 pressed')
            evt.addEvent(Event.K1_PRESSED) 
        else:
            # print('k1 released')
            if time.ticks_diff(time.ticks_ms(),key_time)>LongPressed:
                evt.addEvent(Event.K1_LONG)
            else:                
                evt.addEvent(Event.K1_RELEASED)
    if key==k2:
        if key.value() == 1:
            # print('k2 pressed')
            evt.addEvent(Event.K2_PRESSED)
        else:
            # print('k2 released')
            evt.addEvent(Event.K2_RELEASED)
    if key==k3:
        if key.value() == 0:
            # print('k3 pressed')
            evt.addEvent(Event.K3_PRESSED)
        else:
            # print('k3 released')   
            evt.addEvent(Event.K3_RELEASED)  
    




k1.irq(fun,Pin.IRQ_FALLING | Pin.IRQ_RISING)
k2.irq(fun,Pin.IRQ_FALLING | Pin.IRQ_RISING)
k3.irq(fun,Pin.IRQ_FALLING | Pin.IRQ_RISING)

currentPage=0


  

# syncTimeByWifi(ssid,password)
# sec=time.mktime(time.localtime())#获取时间戳
# now = time.localtime(sec+zonetime)#获取新时区的时间

# rtc.datetime(now)

evt = Event() 
disp.clear()
 
watch = Watch(rtc.datetime())
 
disp.drawTime( 0,0,watch,C_GREEN,C_YELLOW,C_BLACK)

watch.resetTimeout()

def switchPage():
    global currentPage
    if currentPage==0:
        
        for j in range(8):
            disp.drawTime(0,-1-j,watch,C_GREEN,C_YELLOW,C_BLACK)
            disp.drawWeek(0,7-j,watch,C_GREEN,C_BLACK)
            disp.show()
            time.sleep(0.01)
        currentPage=1
        print(currentPage)
        return

    if currentPage==1:
        for j in range(8):
            disp.drawWeek(0,-1-j,watch,C_GREEN,C_BLACK)
            disp.drawDate(0,7-j,watch,C_MONTH,C_DAY,C_BLACK)
            disp.show()
            time.sleep(0.01)
        currentPage=2
        print(currentPage)
        return

    if currentPage==2:
        for j in range(8):
            disp.drawDate(0,-1-j,watch,C_MONTH,C_DAY,C_BLACK)
            disp.drawTime(0,7-j,watch,C_GREEN,C_YELLOW,C_BLACK)
            disp.show()
            time.sleep(0.01)
        currentPage=0
        print(currentPage)
        return

def handleEvent(evt):
    global currentPage     
    if  evt<=0:
        return
    
    if evt==Event.K2_PRESSED:
        switchPage()
        pass
    if evt==Event.K3_PRESSED:
        watch.poweroff()

    if evt==Event.K1_LONG:
        print('syncTimeByWifi')
 
        disp.drawIcon(0,0,15,8,ICON_WIFI,C_BLUE,C_BLACK)
        disp.show()
        syncTimeByWifi(ssid,password)
        sec=time.mktime(time.localtime())#获取时间戳
        now = time.localtime(sec+zonetime)#获取新时区的时间

        rtc.datetime(now)
        if currentPage ==0:
            disp.drawTime(0,0,watch,C_GREEN,C_YELLOW,C_BLACK)            
            updateTime(watch) 
        elif currentPage ==1:
            disp.drawWeek(0,0,watch,C_GREEN,C_BLACK)
        elif currentPage ==2:
            disp.drawDate(0,0,watch,C_MONTH,C_DAY,C_BLACK)

        disp.show()

        print(now)
        pass

 
 
timeout_en = False

if  charge.value()==0 :
    timeout_en = False
else:
    timeout_en = True


print(timeout_en)

 


while True:
    if  charge.value()==0 :
        time.sleep(1.0)
        disp.clear()
        
    if  watch.checkTimeout() and timeout_en:
        print("timeout")
        watch.poweroff()
        watch.resetTimeout()
     

    handleEvent(evt.getEvent())
    # Calculate deadline for operation and test for it
    deadline = time.ticks_add(time.ticks_ms(), 5000)
    if time.ticks_diff(deadline, time.ticks_ms()) > 0:
        deadline = time.ticks_add(time.ticks_ms(), 5000)
        if currentPage ==0:
            updateTime(watch)

         
    
        # print(watch.time_now)
    time.sleep(0.2)
    gc.collect()
    # print(f'mem: {gc.mem_free()}')
