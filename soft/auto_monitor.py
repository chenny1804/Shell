#-*- coding: cp936 -*-
import  telnetlib
import time
UserName="guest"
PassWord="guest"
IP="172.20.186.103"
PORT=23
finish='#'
INTERFACE="wlan1"
DECECT_SSID=["NAP840---TEST4","netcore_chy_2.4","NAP840---TEST1","NAP840---TEST2","NAP840---TEST3"]
# DECECT_SSID=["NAP840---TEST4","NAP840---TEST1","NAP840---TEST2","NAP840---TEST3"]
DURATION=1
COUNT=50
FILE_NAME=time.strftime('%m%d%H%M%S',time.localtime(time.time()))
class Telnet():
    """docstring for Telnet"""
    def __init__(self, username,passwd,ip,port):
        self.username=username
        self.passwd=passwd
        self.ip=ip
        self.port=port
        self.tn = telnetlib.Telnet(self.ip,self.port,timeout=5)
        self.tn.set_debuglevel(0)
    def login(self):
        try:
            self.tn.read_until('login: ',timeout=5)
            self.tn.write(self.username+'\n')
            self.tn.read_until('Password: ',timeout=5)
            self.tn.write(self.passwd+'\n')
            self.tn.read_until(finish)
        except Exception as e:
            print 'telnet not OK',e
            return False
    def write_command(self,command):
        try:
            self.tn.write(command+"\n")
            result=self.tn.read_until(finish)
            print "set command->",command
            return result
        except Exception as e:
            print 'telnet not OK',e
            return False
    def close(self):
        self.tn.close()
def ap_detec():
    tel=Telnet(UserName,PassWord,IP,PORT)
    tel.login()
    tel.write_command("iwpriv "+INTERFACE+" set_mib monitor_en=1")
    tel.write_command("echo 0 >/proc/"+INTERFACE+"/monitor_status")
    tel.write_command("iwpriv "+INTERFACE+" set_mib autoch_ss_cnt=5")
    tel.write_command("iwpriv "+INTERFACE+" set_mib ss_ch_map=8191")
    tel.write_command("iwpriv "+INTERFACE+" set_mib autoch_ss_to=200")
    tel.write_command("iwpriv "+INTERFACE+" set_mib ss_func=15")
    # tel.write_command("iwpriv "+INTERFACE+" autoch report")
    print "sleep 20 second"
    time.sleep(20)
    result=tel.write_command("cat /proc/"+INTERFACE+"/monitor_status")
    return result
def analysis_SSID(result):
    lines=result.split("\n")
    analysis_result=[]
    #f=open("ap_detec.csv","a")
    for line in lines:
        if "SSID" in line:
            SSID=line.split("SSID:")[1].split("RSSI:")[0].strip()
            if SSID in DECECT_SSID:
                line=line.replace(" ","").split(":")
                # print line
                BSS=line[1][:-4]
                SSID=line[2][:-4]
                RSSI=line[3][:-7]
                channel=line[4][:-7]
                Txbytes=line[5].split("\r")[0]
                print BSS,SSID,RSSI,channel,Txbytes
                analysis_result.append(BSS+","+SSID+","+RSSI+","+channel+","+Txbytes)
    return analysis_result
def main():
    f=open("ap_detec_"+FILE_NAME+".csv","a")
    f.write("TIMES,BSSID,SSID,RSSI,Channel,Txbytes\n")
    for i in range(1,COUNT+1):
        print "start count->:",str(i)
        result=ap_detec()
        analysis_result=analysis_SSID(result)
        for result_line in analysis_result:
            f.write(str(i)+","+result_line+"\n")
            f.flush()
        time.sleep(DURATION)
    f.close()
if __name__ == '__main__':
    main()