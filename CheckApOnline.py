# -*- coding: cp936 -*-
import os
def CheckApOnline(filename):
    f=open(filename,"r")
    lines=f.readlines()
    f.close()
    #print lines
    for line in lines:
        if not line.find("#"):
            continue
        st=line.split("\n")[0]
        ip1="0x"+st[0:2]
        ip2="0x"+st[-2:]
        ip1=int(ip1,16)
        ip2=int(ip2,16)
        ip="169.254."+str(ip1)+"."+str(ip2)
        print ip
        f=open("CheckApOnline.csv","a")
        f.write(st+",")
        f.write(ip+",")
        if ping(ip):
            f.write("Online\n")
        else:
            f.write("Not Online\n")
        f.close()
def ping(dst_ip):
    str1="请求超时"
    str2="无法访问目标主机"
    str3="最短"
    cmd=os.popen("ping "+dst_ip+" -n 2")
    lines=cmd.readlines()
    reply_time=[]
    for line in lines:
            if (str1 in line) or (str2 in line):
                #print line
                return False
            elif str3 in line:
                return True
if __name__=="__main__":
    CheckApOnline("./mac.txt")
