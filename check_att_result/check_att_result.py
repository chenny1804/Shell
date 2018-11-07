# -*- coding: utf-8 -*-
from collections import OrderedDict
import os
def get_files(filepath):
	Files=[]
	for txtFile in os.listdir(filepath):
		if ".txt" in txtFile:
			Files.append(txtFile)
	# print Files
	return Files
def read_file(filename):
	f=open(filename)
	result_dict={}
	for line in f.readlines()[1:]:
		param =line.split("\t")
		result_dict[int(param[0].strip())]=float(param[-1].split("%")[0].strip())
	f.close()
	# print result_dict
	return result_dict
def check_att_result(result_dict,pass_value):
	# new_dict=OrderedDict(sorted(result_dict.items(), key=lambda t: t[0]))
	new_dict=sorted(result_dict,reverse=True)
	# print new_dict
	result_check_list=[]
	for i in new_dict[:-1]:
		# print i
		if result_dict[i] < pass_value and result_dict[i] < result_dict[i-1] and  result_dict[i-1] >= pass_value:
			result_check_list.append(str(i)+"\t"+str(result_dict[i])+"%:\t"+str(i-1)+"\t"+str(result_dict[i-1])+"%")
	# print result_check_list
	return result_check_list
def main(filename):
	upath=unicode(filename,"utf-8")
	filenames_list=get_files(upath)
	for file in filenames_list:
		result_check_list=check_att_result(read_file(upath+"\\"+file),92)
		if len(result_check_list) > 0:
			f=open(upath+"_check_result.txt","a")
			for result_string in result_check_list:
				f.write(file+"\t\t\t"+result_string+"\n")
				f.flush()
			f.close()
if __name__ == '__main__':
	Rx_File=[]
	for i in os.listdir("."):
		print i.decode("gbk").encode("utf-8")
		# print os.path.isdir(i)
		if os.path.isdir(i) and "RX_" in i :
			Rx_File.append(i.decode("gbk").encode("utf-8"))
	print Rx_File
	for File in Rx_File:
		main(File)
	# check_att_result(read_file("B_channel_165_VHT20-MCS7.txt"),92)