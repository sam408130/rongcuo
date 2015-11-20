#!/usr/bin/env python  
#-*-coding:utf-8 -*- 

import anydbm
import os
import pinyin
import re
def pProcess(name):
	newname=name.split(r'\(|（|-')[0].lower()
	return newname



def build(names):
	#names=anydbm.open('E:\\sam_work\\forxuwei\\singerNames.db')
	loop=1
	hash_song=anydbm.open('id_singer.db','n')
	hash_word={}
	
	for song in names:
		song=pProcess(song)
		#if loop>10000:break
		hash_song[str(loop)]=song
		try:
			print loop
			song=song.strip(' ').decode('utf-8')
			for i in song:
				if i>= u'\u4e00' and i<=u'\u9fa5':
					mypinyin=pinyin.get(i)
					#print mypinyin
					if hash_word.has_key(mypinyin):
						temphash=hash_word[mypinyin]
						temphash[str(loop)]='1'
					else:
						temphash={}
						temphash[str(loop)]='1'
						hash_word[mypinyin]=temphash
				if hash_word.has_key(i):
					temphash=hash_word[i]
					temphash[str(loop)]='1'
				else:
					temphash={}
					temphash[str(loop)]='1'
					hash_word[i]=temphash
			loop+=1
		except:
			print song
	hash_word2=anydbm.open('daopai_singer.db','n')
	for key in hash_word:
		keys=hash_word[key].keys()
		tempstr=' '.join(keys)
		hash_word2[key.encode('utf-8')]=tempstr

def mat2hash(mat,temphash):
	for i in mat:
		if temphash.has_key(i):
			temphash[i]+=1
		else:
			temphash[i]=1
	return temphash
def search(query,tag):
	if tag=='song':
		songid=anydbm.open('id_song.db','r')
		daopai=anydbm.open('daopai_song.db','r')
	elif tag=='singer':
		songid=anydbm.open('id_singer.db','r')
		daopai=anydbm.open('daopai_singer.db','r')
	elif tag=='both':
		songid=anydbm.open('id_both.db','r')
		daopai=anydbm.open('daopai_both.db','r')
	counthash={}
	out=[]
	for i in query.decode('utf-8'):
		try:
			if i>= u'\u4e00' and i<=u'\u9fa5':
				idstr2=daopai[pinyin.get(i)]
				ids2=idstr2.split(' ')
			idstr=daopai[i.encode('utf-8')]
			ids=idstr.split(' ')
			counthash = mat2hash(ids,counthash)
		except:
			continue
	keys=sorted(counthash.iteritems(),key=lambda counthash:counthash[1],reverse=True)
	loop=0
	for i in keys:
		
		if loop>100:break
		newsong=songid[i[0]]	
		
		out.append(newsong)
		loop+=1
	return out





if __name__=='__main__':
	data=anydbm.open('name2pr.db','r')
	names=[]
	#for i in data:
		#songs=re.compile(r'\|').split(data[i])
		#for j in songs:
		#	names.append(j)
	build(data.keys())