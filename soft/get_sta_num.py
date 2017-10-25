#-*- coding: cp936 -*-
from get_info import get_active_sta_num
import sys
import time
IP=["192.168.1.1","192.168.1.2","192.168.1.3","192.168.1.4","192.168.1.5","192.168.1.6","192.168.1.7","192.168.1.8","192.168.1.9"]
if __name__=="__main__":
	if len(sys.argv) !=3:
		print "Usage:"
		print "\tget_sta_num.py [IP Addr or A] [TIME]"
		print "PS:get_sta_num.py 192.168.1.2 10"
		print "		 get_sta_num.py A 10"
		sys.exit()
	if sys.argv[1] =="A":
		ip=IP
	else:
		ip=sys.argv[1]
	try:
		Time=int(sys.argv[2])
	except Exception as e:
		print e
	if ip == IP:
		while True:
			total=0
			for sub_ip in ip:
				result=get_active_sta_num(sub_ip)
				if not result:
					continue
				total=total+result
			print "TOTAL STA NUM:",total
			time.sleep(Time)
	else:
		while True:
			total=0
			result=get_active_sta_num(ip)
			if not result:
				continue
			total=total+result
			print "TOTAL STA NUM:",total
			time.sleep(Time)

