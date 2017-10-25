def TransToIp(filename):
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
        f=open("ip.txt","a")
        f.write(st+"\t")
        f.write("169.254."+str(ip1)+"."+str(ip2)+"\n")
        f.close()
        print str(ip1)+"."+str(ip2)
if __name__=="__main__":
    TransToIp("./mac.txt")
    