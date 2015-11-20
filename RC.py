#!/usr/bin/env python  
#-*-coding:utf-8 -*- 
import time
import sys
import re
import daopai
import pinyin
import ldsearch
import math
import calPR
import anydbm
def search_song(song):
	#if songs_hash.has_key(song):return song
	max_cost=math.floor(len(song.decode('utf-8'))/3)+1
	#print max_cost
	related_songs=ldsearch.main(song,int(max_cost),'song')
	#print len(related_songs)
	rc_result=calPR.main_song(related_songs)
	#print rc_result
	return rc_result
def paixu(mat,tag):
	temphash={}
	tempmat=[]
	tempmat1=[]
	if tag=='song':
		score=anydbm.open('songToScore.db','r')
	elif tag=='singer':
		score=anydbm.open('singerToScore.db','r')
	for i in mat:
		try:
			temphash[i]=float(score[i])
		except:
			temphash[i]=0
	
	keys=sorted(temphash.iteritems(),key=lambda temphash:temphash[1],reverse=True)
	for j in keys:
		tempmat.append(j[0])
	return tempmat


def loading():
	global singers_hash,songs_hash
	singers_hash={}
	songs_hash={}
	data=anydbm.open('singerToSongs.db','r')
	#print len(data)
	
	data1=anydbm.open('songToSingers.db','r')
	#print len(data1)
	for i in data:
		songs=re.compile(r'\|').split(data[i])
		singers_hash[i]=songs
	for j in data1:
		singers=re.compile(r'\|').split(data1[j])
		songs_hash[j]=singers
	return singers_hash,songs_hash

def search(singer,song):
	
	if singer in singers_hash:
		songs=singers_hash[singer]
		#print song ,songs[0]
		if song in songs:
			return singer,song,'1'
		else:
			max_cost=math.floor(len(song.decode('utf-8')))-1
			related_songs=ldsearch.main(song,int(max_cost),'song')
			#for k in related_songs:print k[0]
			for j in related_songs:
				sub_song=j[0].encode('utf-8')
				if sub_song in songs:
					return singer,sub_song,'2'
				if song == sub_song:
					if song in songs_hash:
						return songs_hash[song][0],song,'3'
			rc_result=calPR.main_song(related_songs)
			#print rc_result.decode('utf-8')
			#try:
			return singer,singers_hash[singer][0],'4'
			#except:
				#return 'null',rc_result
	else:
		if song in songs_hash:
			singers=songs_hash[song]
			max_cost=(len(singer.decode('utf-8')))-1
			related_singers=ldsearch.main(singer,max_cost,'singer')
			for j in related_singers:
				sub_singer=j[0].encode('utf-8')
				
				if sub_singer in singers:
					
					return sub_singer,song,'5'
			rc_result=calPR.main_singer(related_singers)
			return rc_result,song,'6'
		else:
			return 'null','null','7'







if __name__=='__main__':
	#print 'loading...'
	#loading()
	#print 'loading completed...'
	'''
	data=open('E:\\sam_work\\12530\\Tpairs.txt','r')
	timeuse=[]
	match=0
	unmatch=0
	out=open('rongcuo_result.txt','w')
	#data=['周乐_浪花']
	for i in data:
		i=i.strip('\n')
		mat=re.compile('_').split(i)
		start = time.time()
		
		singer,song,tag=search(mat[0],mat[1])
		print singer.decode('utf-8'),song.decode('utf-8')
		end = time.time()
		timeuse.append(float(end-start))
		if singer==mat[0] and song==mat[1]:
			match+=1
		else:
			unmatch+=1
			out.write(i+'       rongcuo_result:'+'%s_%s'%(singer,song)+'       %s'%tag+'\n')
	print 'average time : %d'%(sum(timeuse)/len(timeuse))
	print 'match  %d'%match
	print 'unmatch  %d'%unmatch
	
	mat1=re.compile(r'_').split('痛彻心扉_西单女孩')
	singer,song,tag=search(mat1[1],mat1[0])
	print singer.decode('utf-8')
	print song.decode('utf-8')
	print tag
	'''
	song = '望故乡'
	rc = search_song(song)
	print rc.decode('utf-8')