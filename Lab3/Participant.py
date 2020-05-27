import socket

import sys

class Participant:

    def __init__(self,ip,port,selfip,selfport):

        self.ip=ip

        self.port=port

        self.myip=selfip

        self.myport=selfport

        self.connlist=[]

        self.mylog=[]

        self.KV_Store={}

        self.s=socket.socket()

        self.state=1

    def setListenPort(self):

        #端口强制复用

        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)

        self.s.bind((self.myip,int(self.myport)))

        self.s.listen(10)

    def mydecode(self,str):

        arr=[]

        paras=str.split('\r\n')

        for id,item in enumerate(paras):

            if(id%2==0 and id!=0):

                arr.append(item)

        return arr

    def connectall(self):

        arr=[]

        for id,item in enumerate(self.ip):

            ss=socket.socket()

            ss.connect((self.ip[id],int(self.port[id])))

            #print("try to connect:%s:%s"%(self.ip[id],self.port[id]))

            arr.append(ss)

        return arr

    def closeall(self,arr):

        for soc in arr:

            soc.close()

    def TPC_Participant(self):

        self.setListenPort()

        while True:

        #State1:initial

            #State1:init

            if(self.state==1):

                conn,srcip=self.s.accept()

                message=conn.recv(1024).decode('utf-8')

                #print("I have receive A message")

                #print(message)

                if( message.startswith('*')):

                    self.connlist=self.connectall()

                    #conn.send("+Ok\r\n".encode('utf-8'))

                #conn.close

                else:

                    continue

                para=self.mydecode(message)

                #print("the message has"+str(len(para))+"len")

                #print("I have receive A Job")

                if(para[0]=="SET" or para[0]=='GET' or para[0]=='DEL'):

                    #print("I am ready")

                    self.connlist[0].sendall("Prepared".encode('utf-8'))

                    #mylog.append(str(state))

                    for item in para:

                        self.mylog.append(item)   

                    self.state=2

            #State2:get request

            elif(self.state==2):

                #print("wait for Admit")

                conn,srcip=self.s.accept()

                message=conn.recv(1024).decode('utf-8') 

                #conn.close
                #print(message)
            

                if(message=="Admit"):

                    #print("get Admit")

                    #print(self.mylog)

                    self.connlist=self.connectall()

                    if self.mylog[0]=="SET":

                        self.KV_Store[self.mylog[1]]=self.mylog[2]

                        self.connlist[0].sendall("DONE +OK\r\n".encode('utf-8'))

                    elif self.mylog[0]=='GET' and self.KV_Store.get(self.mylog[1],0)!=0:

                        #str_pes="DONE *1\r\n$"+str(len(KV_Store[mylog[1]]))+KV_Store[mylog[1]+"\r\n"

                        #myconnect((ip[0],int(port[0])),"DONE *1\r\n")

                        self.connlist[0].sendall(("DONE *1\r\n$"+str(len(self.KV_Store[self.mylog[1]]))+"\r\n"+self.KV_Store[self.mylog[1]]+"\r\n").encode('utf-8'))

                    elif self.mylog[0]=='GET' and self.KV_Store.get(self.mylog[1],0)==0:

                        #myconnect((ip[0],int(port[0])),"DONE "+"*1\r\n$3\r\nnil\r\n")

                        self.connlist[0].sendall(("DONE *1\r\n$3\r\nnil\r\n").encode('utf-8'))

                    elif self.mylog[0]=='DEL':

                        z=0

                        i=1

                        while i<len(self.mylog):

                            if(self.KV_Store.get(self.mylog[i],0)!=0):

                                del self.KV_Store[self.mylog[i]]

                                z+=1

                                i+=1

                            else:

                                i+=1

                                continue

                        #myconnect((ip[0],int(port[0])),"DONE "+str(z))

                        self.connlist[0].sendall(("DONE :"+str(z)+"\r\n").encode('utf-8'))

                    else:

                        #myconnect((ip[0],int(port[0])),"DONE -ERROR\r\n")

                        self.connlist[0].sendall("DONE -ERROR\r\n".encode('utf-8'))

                    self.mylog.clear()

                    #self.closeall(self.connlist)

                    self.state=1

                elif(message=="Abort"):

                    self.mylog.clear()

                    self.state=1

        self.closeall(self.connectall)    
