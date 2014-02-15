#!/usr/bin/env python

from lxml import etree
import urllib
import sys
import os

class FRTvurl():
	id_video=0
	url='http://www.francetvinfo.fr/appftv/webservices/video/getInfosOeuvre.php?id-diffusion='
	video_url=''
	idv=0
	def __init__(self,id_video):
		self.id_video=id_video
	def get_url(self):
		return self.id_video
	def parse_url(self):
		data=urllib.urlopen("%s%s"%(self.url,self.id_video)).read()
		root=etree.XML(data)
		url=root.xpath('//url/text()')[0]
		url=url.replace('/z/','/i/')
		url=url.replace('manifest.f4m', 'index_2_av.m3u8')
		self.video_url=url
		self.idv=0
	def getbloc(self):
		self.mkdir()	
		self.parse_url()
		data=urllib.urlopen(self.video_url)
		block=[]
		for i in data:
			 if (i[0]!='#'):
				block.append(i.strip())

		for idv,url in enumerate(block):
			self.download(idv,len(block),url)
##		ffmpeg -i <(cat *ts) -vcodec copy  $(basename `pwd`).mp4
		
	
	def download(self,idx,_all,url):
		sys.stdout.write("\r")
		sys.stdout.write("[")
		x = int(100*idx/_all)
		inner_bar = ['#' for i in range(int(x/2))] + ["." for i in range(50 - int(x/2))]
		sys.stdout.write("".join(inner_bar))
		sys.stdout.write("]")
		sys.stdout.write(" "+str(x))
		sys.stdout.write("%")
		sys.stdout.flush()
		urllib.urlretrieve(url,'Part%06d.ts'%idx);
	def mkdir(self):
		os.mkdir(str(self.id_video))
		os.chdir(str(self.id_video))
			

vid=FRTvurl(sys.argv[1])
vid.getbloc()
