
from socket import *
import thread
import datetime
from DBConnection import DBConnect
import re

d=DBConnect()
BUFF = 1024
HOST ='localhost'
PORT = 505
result=[]
r1=[]

def response(key):
    return  key

def handler(clientsock,addr):
    while 1:
        try:
            del r1[:]
            data = clientsock.recv(BUFF)
            print "DataReceived:" + data
            if not data: break

            result = data.split('*')
            for re2 in result:
                equipmentUnit = re2.split(",", 1)[0]
            for item in re2.split(','):
                r1.append(re.sub("[^\w\-\d\.\/\:\+]", "", item))
            r1.pop(0)
            print repr(addr) + ' recv:' + repr(data)
            startTime = datetime.datetime.now()
            print "Time:"+ str(startTime)
            if "close" == data.rstrip(): break
            if equipmentUnit == 'K0':
                d.Login_Insert(equipmentUnit,addr[1],addr[0],r1[0])
            elif equipmentUnit=='K1':
                d.SamplingData(equipmentUnit,addr[1],addr[0],r1[0],r1[1],r1[2],r1[3],r1[4],r1[5],r1[6])
            elif equipmentUnit=='K2':
                d.PowerWater(equipmentUnit,addr[1],addr[0],r1[0],r1[1],r1[2])
            elif equipmentUnit=='K3':
                d.TimeDuration(equipmentUnit,addr[1],addr[0],r1[0])
                clientsock.send(response("*" + equipmentUnit +','+str(datetime.datetime.now().strftime("%H:%M:%S"))+ "#"))
                continue
            elif equipmentUnit == 'K4':
                d.FilteringTime(equipmentUnit,addr[1],addr[0],r1[0],r1[1],r1[2],r1[3],r1[4],r1[5],r1[6],r1[7])
            elif equipmentUnit == 'K5':
                d.ErrorMessage(equipmentUnit,addr[1],addr[0],r1[0],r1[1],r1[2])
            clientsock.send(response("*" + equipmentUnit + ",1#"))

        except Exception,e:
            print str(e)
            clientsock.sendall(response("Error in Sending data"))
    clientsock.close()
    print addr, "- closed connection" #log on console
    print "............"
    print ""


if __name__=='__main__':
    ADDR = (HOST, PORT)
    serversock = socket(AF_INET, SOCK_STREAM)
    serversock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    serversock.bind(ADDR)
    serversock.listen(5)
    while 1:
        print 'waiting for connection... listening on port', PORT
        clientsock, addr = serversock.accept()
        print 'connected from:', addr
        thread.start_new_thread(handler, (clientsock, addr))



