import os
cmd=os.popen("netsh wlan show interfaces")
lines=cmd.readlines()
#print lines
for line in lines:
    f=open("./interfacesInfo.txt","a")
    print line
    f.write(line+"\n")
    f.close()
