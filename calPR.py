#!/usr/bin/env python  
#-*-coding:utf-8 -*- 
import time
import sys
import re
import anydbm
import math
def main_song(mat):
	score=anydbm.open('name2pr.db','r')
	tempscore=0
	finalresult=''
	for i in mat:
		if i[1]==0:
			return i[0].encode('utf-8')
		if score.has_key(i[0].encode('utf-8')):
			pr=score[i[0].encode('utf-8')]
		else:
			pr=0
		
		combi=(float(pr)+0.000001)/(math.pow(10,i[1])+0.000001)
		#print i[0],float(pr),i[1],combi
		if combi>tempscore:
			tempscore=combi
			finalresult=i[0].encode('utf-8')
	return finalresult
def main_singer(mat):
	score=anydbm.open('singerToScore.db','r')
	tempscore=0
	finalresult=''
	for i in mat:
		if score.has_key(i[0].encode('utf-8')):
			pr=score[i[0].encode('utf-8')]
		else:
			pr=0
		combi=(float(pr)+0.000001)/((10^i[1])+0.000001)
		if combi>tempscore:
			tempscore=combi
			finalresult=i[0].encode('utf-8')
		#except:
			#continue
	return finalresult