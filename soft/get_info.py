#-*- coding: cp936 -*-
import  telnetlib
import time
UserName="guest"
PassWord="asdfghjkl"
def telnet_command(username,passwd,ip,port,command):
    finish='#'
    try:
        tn=telnetlib.Telnet(ip,port,timeout=5)
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
        #print 'telnet not OK',e
        return False
def get_interface_active_num(ip,interface):
    active_num=telnet_command(UserName,PassWord,ip,23,"cat /proc/"+interface+"/sta_info | grep active")
    if active_num:
        return int(active_num.split("\n")[1].split(":")[1].split(")")[0])
    else:
        return False
def get_active_sta_num(ip):
    num_2_4G=get_interface_active_num(ip,"wlan1")
    num_5G=get_interface_active_num(ip,"wlan0")
    if not num_2_4G and not num_5G:
        print "telnet "+ip+" not OK "
        return False
    else:
        print ip
        print "\t2.4G->",num_2_4G
        print "\t  5G->",num_5G
        return int(num_2_4G)+int(num_5G)
def get_interface_rssi(ip,interface):
    Interface_Rssi=telnet_command(UserName,PassWord,ip,23,"cat /proc/"+interface+"/sta_info | grep rssi")
    if Interface_Rssi:
        return Interface_Rssi
    else:
        #print ip+" telnet not OK "
        return False
def get_sta_rssi(ip):
    Rssi_2_4G=get_interface_rssi(ip,"wlan1")
    #print Rssi_2_4G
    Rssi_5G=get_interface_rssi(ip,"wlan0")
    if not Rssi_2_4G and not Rssi_5G:
        print "telnet "+ip+" not OK "
        return False
    print ip
    print "   2.4G RSSI"
    for rssi in Rssi_2_4G.split("\n"):
        if rssi.find("rssi:")>0:
            print "\t"+rssi.split("rssi:")[1]
    print "   5G RSSI"
    for rssi in Rssi_5G.split("\n"):
        if rssi.find("rssi:")>0:
            print "\t"+rssi.split("rssi:")[1]
    return True
def get_interface_rssi_dump(ip,interface):
    Rssi_dump=telnet_command(UserName,PassWord,ip,23,"cat /proc/"+interface+"/rssi_dump")
    if Rssi_dump:
        return Rssi_dump
    else:
        #print "telnet "+ip+" not OK "
        return False
def get_sta_rssi_dump(ip):
    Rssi_dump_2_4G=get_interface_rssi_dump(ip,"wlan1")
    Rssi_dump_5G=get_interface_rssi_dump(ip,"wlan0")
    if not Rssi_dump_2_4G and not Rssi_dump_5G:
        print "telnet "+ip+" not OK"
        return False
    print ip," 2.4G"
    print "\tRssi \tretry\t\tTxRate\tRxRate FA \tCCA"
    for rssi_dump in Rssi_dump_2_4G.split("\n"):
        if rssi_dump.find("%")>0:
            rssi_list=rssi_dump.split(" ")
            #print rssi_list
            print "\t"+rssi_list[1]+"\t",rssi_list[2]+"\t",rssi_list[4]+"\t",rssi_list[6]+"\t",rssi_list[11].split(")")[0]+"\t",rssi_list[12].split(")")[0]+"\t"
    print ip," 5G"
    print "\tRssi \tretry\t\tTxRate\tRxRate FA \tCCA"
    for rssi_dump in Rssi_dump_5G.split("\n"):
        if rssi_dump.find("%")>0:
            rssi_list=rssi_dump.split(" ")
            print "\t"+rssi_list[1]+"\t",rssi_list[2]+"\t",rssi_list[4]+"\t",rssi_list[6]+"\t",rssi_list[11].split(")")[0]+"\t",rssi_list[12].split(")")[0]+"\t"
    return True
def get_interface_byte(ip,interface):
    speed_wlan0=telnet_command(UserName,PassWord,ip,23,"ifconfig "+interface)
    if speed_wlan0:
        rx=speed_wlan0.split("\n")[6].split(" (")[0].split(":")[1]
        tx=speed_wlan0.split("\n")[6].split(" (")[1].split(":")[1]
        return int(rx),int(tx)
    else:
        return False,False
def get_interface_speed(ip,interface):
    T1=time.time()
    (Rx1,Tx1)=get_interface_byte(ip,interface)
    if not Rx1 and not Tx1:
        print "telnet "+ip+" not OK "
        return False,False
    T2=time.time()
    (Rx2,Tx2)=get_interface_byte(ip,interface)
    Rx_speed=(Rx2-Rx1)/((T2-T1)*1024)
    Tx_speed=(Tx2-Tx1)/((T2-T1)*1024)
    return Rx_speed,Tx_speed
def get_speed(ip):
    (Rx_2_4G_speed,Tx_2_4G_speed)=get_interface_speed(ip, "wlan1")
    if not Rx_2_4G_speed and not Tx_2_4G_speed:
        return False
    (Rx_5G_speed,Tx_5G_speed)=get_interface_speed(ip, "wlan0")
    print ip
    print "2.4G Rx",Rx_2_4G_speed,"2.4G Tx",Tx_2_4G_speed
    print "  5G Rx",Rx_5G_speed,"  5G Tx",Tx_5G_speed
if __name__=="__main__":
    get_speed("192.168.1.1")