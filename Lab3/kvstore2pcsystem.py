import socket
import sys
import Util
import Participant
import Coordinator
ROLE,myip,myport,ip,port=Util.R_Conf(sys.argv)
#print(myip,myport)
if ROLE==1:
    coor=Coordinator.Coordinator(ip,port,myip,myport)
    coor.TPC_Coordinator()
elif ROLE==0:
    part=Participant.Participant(ip,port,myip,myport)
    part.TPC_Participant()
