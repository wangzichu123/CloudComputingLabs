import socket
import sys
def R_Conf(argv):
    conf=[]
    ip=[]
    port=[]
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
	    ##print("yes")
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
    ##print(ROLE)
    ##print(myip,myport)
    #for id,item in enumerate(ip):
        ##print(item,port[id])
    return ROLE,myip,myport,ip,port
