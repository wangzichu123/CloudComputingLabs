import socket
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
        #print("try to connect:%s"%arr2[id])
        arr.append(ss)
    return arr
