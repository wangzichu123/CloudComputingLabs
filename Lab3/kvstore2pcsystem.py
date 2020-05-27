import socket
import sys

#Read Conf file to bind ip:port
conf=[]
ip=[]
port=[]
myip=""
myport=""
par_num=2
global mylog
global clientconn
mylog=[]
#ROLE=1:Coordinator;ROLE=0:Particpant
ROLE=-1
def R_Conf(argv,ROLE):
    conf_file_name=argv[2]
    for line in open(conf_file_name):
        if not line.startswith('!'):
            line=line.strip('\n')
            conf.append(line)
    myip=""
    myport=""
    for line in conf:
        role=line.split(' ')
        if(role[0]=="mode"and role[1]=="participant" ):
            	ROLE=0
        elif(role[0]=="mode" and role[1]=="coordinator"):
            	ROLE=1
        elif(ROLE==0 and role[0]=="participant_info"):
            ip_port=role[1].split(':')
            myip=ip_port[0]
            myport=ip_port[1]
        elif (ROLE==1 and role[0]=="coordinator_info"):
            ip_port=role[1].split(':')
            myip=ip_port[0]
            myport=ip_port[1]
        elif(ROLE==0 and role[0]=="coordinator_info"):
            ip_port=role[1].split(':')
            ip.append(ip_port[0])
            port.append(ip_port[1])
        elif(ROLE==1 and role[0]=="participant_info"):
            ip_port=role[1].split(':')
            ip.append(ip_port[0])
            port.append(ip_port[1])
    return ROLE,myip,myport
def mydecode(str):
    arr=[]
    paras=str.split('\r\n')
    for id,item in enumerate(paras):
        if(id%2==0 and id!=0):
            arr.append(item)
    return arr
def connectall(arr1,arr2):
    arr=[]
    for id,item in enumerate(arr1):
        ss=socket.socket()
        ss.connect((arr1[id],int(arr2[id])))
        arr.append(ss)
    return arr
ROLE,myip,myport=R_Conf(sys.argv,ROLE)
##print(myip,myport)
if ROLE==0:
    myconnect=[]
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    s.bind((myip,int(myport)))
    s.listen(10)
    KV_Store={}
    state=1
    while True:
        #State1:init
        if(state==1):
            conn,srcip=s.accept()
            message=conn.recv(1024).decode('utf-8')
            if( message.startswith('*')):
                myconnect=connectall(ip,port)
                para=mydecode(message)
                conn.send("+Ok\r\n".encode('utf-8'))
            #conn.close
            para=mydecode(message)
            if(para[0]=="SET" or para[0]=='GET' or para[0]=='DEL'):
                myconnect[0].sendall("Prepared".encode('utf-8'))
                for item in para:
                    mylog.append(item)   
                state=2
        #State2:get request
        elif(state==2):
            conn,srcip=s.accept()
            message=conn.recv(1024).decode('utf-8') 
            #conn.close
            
            if(message=="Admit"):
                myconnect=connectall(ip,port)
                if mylog[0]=="SET":
                    KV_Store[mylog[1]]=mylog[2]
                    myconnect[0].sendall("DONE +OK\r\n".encode('utf-8'))
                elif mylog[0]=='GET' and KV_Store.get(mylog[1],0)!=0:
                    myconnect[0].sendall(("DONE *1\r\n$"+str(len(KV_Store[mylog[1]]))+"\r\n"+KV_Store[mylog[1]]+"\r\n").encode('utf-8'))
                elif mylog[0]=='GET' and KV_Store.get(mylog[1],0)==0:
                    myconnect[0].sendall(("DONE *1\r\n$3\r\nnil\r\n").encode('utf-8'))
                elif mylog[0]=='DEL':
                    z=0
                    i=1
                    while i<len(mylog):
                        if(KV_Store.get(mylog[i],0)!=0):
                            del KV_Store[mylog[i]]
                            z+=1
                            i+=1
                        else:
                            i+=1
                            continue
                    #myconnect((ip[0],int(port[0])),"DONE "+str(z))
                    myconnect[0].sendall(("DONE :"+str(z)+"\r\n").encode('utf-8'))
                else:
                    #myconnect((ip[0],int(port[0])),"DONE -ERROR\r\n")
                    myconnect[0].sendall("DONE -ERROR\r\n".encode('utf-8'))
                mylog.clear()
                state=1
            elif(message=="Abort"):
                mylog.clear()
                state=1        
    s.close
elif ROLE==1:
    myconect=[]
    
    num=len(ip)
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    s.bind((myip,int(myport)))
    s.listen(10)
    i=0
    state=1
    para=[]
    while True:
        if(state==1):
            conn,srcip=s.accept()
            message=conn.recv(1024).decode('utf-8')
            if( message.startswith('*')):
                clientconn=conn
                myconect=connectall(ip,port)
                para=mydecode(message)
            if(para[0]=="SET" or para[0]=='GET' or para[0]=='DEL'):
                for i in range(num):
                    myconect[i].sendall(message.encode('utf-8'))
                state=2
                i=0
        elif(state==2):
            conn,srcip=s.accept()
            message=conn.recv(1024).decode('utf-8')
            if(message=="Prepared"):
                i=i+1
            if(i==len(ip)):
                myconect=connectall(ip,port)
                for i in range(len(ip)):
                    myconect[i].sendall("Admit".encode('utf-8'))
                state=3
                i=0
        elif(state==3):
            conn,srcip=s.accept()
            message=conn.recv(1024).decode('utf-8')
            mes=message.split(' ')
            if(mes[0]=="DONE"):
                i=i+1
                mylog.append(mes[1])
            if(i==len(ip)):
                clientconn.sendall(mylog[0].encode('utf-8'))
                mylog.clear()
                state=1
        #State3:Abort or Commit
        #Abort
    for i in range(num):
        myconnect[i].close
    s.close
