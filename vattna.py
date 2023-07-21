from machine import Pin
import utime

re1 = Pin(2, Pin.OUT)
re2 = Pin(3, Pin.OUT)
re3 = Pin(4, Pin.OUT)
re4 = Pin(5, Pin.OUT)

re1.value(False)
re2.value(False)
re3.value(False)
re4.value(False)


def vattna(channel,maxtime):
    start=utime.ticks_ms()      
    if channel==1:
        re1.value(True)
    elif channel==2:
        re2.value(True)
    elif channel==3:
        re3.value(True)
    elif channel==4:
        re4.value(True)
    
    while (True):
        if (utime.ticks_ms()-start)/1000>maxtime:
            break
        utime.sleep_ms(500)
        print(channel, ',' , round((utime.ticks_ms()-start)/1000))
    
    if channel==1:
        re1.value(False)
    elif channel==2:
        re2.value(False)
    elif channel==3:
        re3.value(False)
    elif channel==4:
        re4.value(False)
    
    



