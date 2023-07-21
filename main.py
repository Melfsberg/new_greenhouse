import machine
import network
import socket
import time
import utime
import webpage
import struct
import _thread
import vattna
import secrets

rtc=machine.RTC()

DEFTIMESTR=[]
DEFDUR=[]
DEFCNT=[]
timestr=[]
dur=[]
cnt=[]
systime=[]

def set_time():
    NTP_DELTA = 2208981600
    host = "pool.ntp.org"
    NTP_QUERY = bytearray(48)
    NTP_QUERY[0] = 0x1B
    addr = socket.getaddrinfo(host, 123)[0][-1]
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.settimeout(1)
        res = s.sendto(NTP_QUERY, addr)
        msg = s.recv(48)
    finally:
        s.close()
    val = struct.unpack("!I", msg[40:44])[0]
    t = val - NTP_DELTA    
    tm = time.gmtime(t)
    machine.RTC().datetime((tm[0], tm[1], tm[2], tm[6] , tm[3], tm[4], tm[5], 0))
    print("updated")

def control_thread():
    global dur,cnt,systime
    slinga=[]
    while True:
        rtc_time=rtc.datetime()[4:7]
        systime="%02d" % rtc_time[0] + ":" + "%02d" % rtc_time[1] + ":" "%02d" % rtc_time[2]
        
        if systime in timestr:
            slinga=timestr.index(systime)
            cnt[slinga]=str(int(cnt[slinga])+1001)[1:4]
            
            if int(dur[slinga])>0:
                vattna.vattna(int(slinga+1),int(dur[slinga]))
        time.sleep(.1)                        
        
def set_default():
    global DEFTIMESTR,DEFDUR,DEFCNT    
    DEFTIMESTR=['16:00:00','16:05:00','16:10:00','16:15:00']
    DEFDUR=['060','050','045','000']
    DEFCNT=['000','000','000','000']

def check_time_input(tid):
    if len(tid)==8:
        if tid[5]==tid[2]==':':
            if int(tid[0:2]) < 24:                
                if int(tid[3:5])<60:
                    if int(tid[6:8])<60:                    
                        return True
                    else:
                        return False    
            else:
                return False
        else:
            return False
    else:
        return False

def check_dur_input(dur):
    try:
        num=int(dur)
    except ValueError:
        return False
    if num>999:
        return False    
    return True

def test(slinga,cnt):
    print(slinga)
    vattna.vattna(int(slinga),10)
    return str(int(cnt)+1001)[1:4]

wlan=network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(secrets.ssid,secrets.password)

wait=10
while wait>0:
    if wlan.status() < 0 or wlan.status() > 3:
        break
    wait -=1
    print('waiting for connection...')
    time.sleep(.1)
    
if wlan.status() !=3:
    raise RuntimeError('wifi connection failed')
else:
    print('connected')
    ip=wlan.ifconfig()[0]
    print('IP: ', ip)

_thread.start_new_thread(control_thread,())
set_time()

def serve(connection):
    global timestr,dur,cnt
    init=True
    i=[0]*12
    
    while True:
        client = connection.accept()[0]
        request = client.recv(1024)
        request = str(request)
        try:
            request.split()[1]
        except IndexError:
            pass
        
        print(request)     
        
        if not init:
            i[0]=request.find('time1=',0,160)
            i[1]=request.find('dur1=',0,160)
            i[2]=request.find('cnt1=',0,160)        
            i[3]=request.find('time2=',0,160)
            i[4]=request.find('dur2=',0,160)
            i[5]=request.find('cnt2=',0,160)        
            i[6]=request.find('time3=',0,160)
            i[7]=request.find('dur3=',0,160)
            i[8]=request.find('cnt3=',0,160)        
            i[9]=request.find('time4=',0,160)
            i[10]=request.find('dur4=',0,160)
            i[11]=request.find('cnt4=',0,160)            
         
            for n in range(0,10,3):
                temp=request[i[n]+6:i[n+1]-1].replace('%3A',':')
                if check_time_input(temp):
                    timestr[int(n/3)]=temp              
                temp=request[i[n+1]+5:i[n+2]-1]
                if check_dur_input(temp):
                    dur[int(n/3)]=temp
            
        if request.find('/time',0,20)!=-1:            
            print("update time")
            set_time()
                
        if init:
            set_default()
            timestr=DEFTIMESTR
            dur=DEFDUR
            cnt=DEFCNT
            init=False
           
        if request.find('/reset',0,20) !=-1:
            cnt=['000','000','000','000']
            
        if request.find('/test',0,20)!=-1:        
            temp=request.find('/test',0,20)
            pos=int(request[temp+5])
            cnt[(pos-1)]=test(pos,cnt[pos-1])
           
        print('---------------------------------------------------------')
        print(timestr, '\n', dur, '\n',  cnt)
        
        html=webpage.webpage(systime,timestr,dur,cnt)
        
        client.send(html)
        client.close()
        
def open_socket(ip):
    address = (ip, 80)
    connection = socket.socket()
    connection.bind(address)
    connection.listen(1)
    print(connection)
    return(connection)
try:
    if ip is not None:
        connection=open_socket(ip)
        serve(connection)
except KeyboardInterrupt:
    machine.reset()            
            
