import socket

import sys

class Coordinator:

    def __init__(self,ip,port,selfip,selfport):

        self.ip=ip

        self.port=port

        self.myip=selfip

        self.myport=selfport

        self.connlist=[]

        self.mylog=[]

        self.s=socket.socket()

        self.state=1

        self.clientlist=[]

    def setListenPort(self):

        #端口强制复用

        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)

        self.s.bind((self.myip,int(self.myport)))

        self.s.listen(10)

    def mydecode(self,mstr):

        arr=[]

        paras=mstr.split('\r\n')

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

    def TPC_Coordinator(self):

        self.setListenPort()

        while True:

        #State1:initial

            if(self.state==1):

                conn,srcip=self.s.accept()

                message=conn.recv(1024).decode('utf-8')

                #print("I have receive A message")

                ##print(message)

                if( message.startswith('*')):

                    self.clientlist.clear()

                    self.clientlist.append(conn)

                    self.connlist=self.connectall()
                else:
                    continue

                para=self.mydecode(message)

                #print("the message has"+str(len(para))+"len")

                if(para[0]=="SET" or para[0]=='GET' or para[0]=='DEL'):
              
                    #print("the connlist size%s"%len(self.connlist))

                    for i in range(len(self.connlist)):

                        self.connlist[i].sendall(message.encode('utf-8'))
                        
                    #print("I have Send message to participant")

                    self.state=2

                    i=0

                    self.closeall(self.connlist)

            elif(self.state==2):

                conn,srcip=self.s.accept()

                message=conn.recv(1024).decode('utf-8')

                if(message=="Prepared"):

                    i=i+1

                    #print("I have receive A prepared")

                if(i==len(self.ip)):

                    #print("try to send Admit")

                    self.connlist=self.connectall()

                    for id in range(len(self.ip)):

                        self.connlist[id].sendall("Admit".encode('utf-8'))
                        
                        #print("now send"+str(id))

                    self.state=3

                    i=0
                     
                    self.closeall(self.connlist)

            elif(self.state==3):

                #print("try to acquire the result")

                conn,srcip=self.s.accept()

                message=conn.recv(1024).decode('utf-8')

                mes=message.split(' ')

                if(mes[0]=="DONE"):

                    i=i+1

                    #print("I have get a result%s"%mes[1])

                    self.mylog.append(mes[1])

                if(i==len(self.ip)):

                    #myconnect(srcip,mylog[0])

                    #print("I have get all result")

                    self.clientlist[0].sendall(self.mylog[0].encode('utf-8'))

                    self.mylog.clear()

                    self.state=1

            #State3:Abort or Commit

            #Abort

        #closeall(self.connlist)


