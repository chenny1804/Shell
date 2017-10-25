#-*- coding: cp936 -*-
import  telnetlib
def telnet_command(username,passwd,ip,port,command):
    finish='#'
    try:
        tn=telnetlib.Telnet(ip,port,timeout=10)
        tn.set_debuglevel(0)
        tn.read_until('login: ',timeout=5)
        tn.write(username+'\n')
        tn.read_until('Password: ',timeout=5)
        tn.write(passwd+'\n')
        tn.read_until(finish)
        tn.write(command+'\n')
        d=tn.read_until(finish)
        tn.close()
        return d
    except Exception as e:
        print 'telnet not OK',e
        return False
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
                return line
            elif str3 in line:
                for i in line.split('，'):
                    st=i.split('= ')[1]
                    #print st
                    reply_time.append(st.split('ms')[0])
    #print reply_time
    return reply_time
def main():
	version=telnet_command("guest","guest","192.168.1.6",23,"cat /tmp/version")
	if version:
            version=version.split("\n")[1]
            print version
if __name__=="__main__":
	main()