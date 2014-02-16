#!/usr/bin/env python

from lxml import etree
import urllib
import sys
import os
import progress
import glob
import thread
import time
import subprocess

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
		titre=root.xpath('//titre/text()')[0]
		print titre
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
		progressb=progress.progressbar(len(block))

		for idv,url in enumerate(block):
			progressb.display(idv)
			self.download(idv,len(block),url)
##		ffmpeg -i <(cat *ts) -vcodec copy  $(basename `pwd`).mp4
		
	
	def download(self,idx,_all,url):
		urllib.urlretrieve(url,'Part%06d.ts'%idx);
	def mkdir(self):
		os.mkdir(str(self.id_video))
		os.chdir(str(self.id_video))
			
	def concatfile(self):
	        if (os.path.exists('dd.fifo')):
	                os.unlink('dd.fifo')
	        os.mkfifo('dd.fifo')
	
	        tb=glob.glob('*.ts')
	        tb.sort()
	        p=progress.progressbar(len(tb))
	        for n,name in enumerate(tb):
	                p.display(n)
	                open('dd.fifo','wb').write(open(name,'rb').read())
	def clean(self):
		tb=glob.glob('*.ts')
		p=progress.progressbar(len(tb))
		os.unlink('dd.fifo')
		for n,name in enumerate(tb):
			p.display(n)
			os.unlink(name)
			

vid=FRTvurl(sys.argv[1])
vid.getbloc()

thread.start_new_thread(vid.concatfile,());
print "\nConvert"
time.sleep(10)
args=['ffmpeg','-y','-i','dd.fifo','-vcodec','copy',str(sys.argv[1])+'.mp4']
p=subprocess.call(args,stdout=subprocess.PIPE,stderr=subprocess.PIPE)

print "\nClean"
vid.clean()
