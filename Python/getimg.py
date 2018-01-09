#! /usr/bin/env python
# -*- coding:utf-8 -*-

import urllib2
import re
import os
import cv2
import json

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import codecs

#import put_chinese_text as pct
import pdb
import win32process, win32event

class Getimage(object):
    def __init__(self):
        self.filepath = 'G:\\bingImage\\today.jpg'
        self.txtpath = 'G:\\bingImage\\today.txt'
        self.bmppath = 'G:\\bingImage\\today.bmp'
        self.basepath = 'http://www.bing.com'
        self.imgurl = 0
        
        #self.ft = pct('wqy-zenhei.ttc')

    def crawb(self):
        print 'analyzing web data...',
        html = urllib2.urlopen('http://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=zh-CN').read()
        #self.imgurl = re.findall('http[^"]*?1920x1080.jpg', html)
        self.imgurl = json.loads(html)['images'][0]['url']
        self.copyright = json.loads(html)['images'][0]['copyright'].split()[0]
        print 'done'

    def downloadimg(self):
        print 'saving picture...'
        count = 0
        for url in self.imgurl:
            try:
                img = urllib2.urlopen(url).read()
                file = open(self.filepath,'wb')
                file.write(img)
                count += 1
            finally:
                file.close()
            if count >= 1:
                break
        if count >= 1:
            print '%d picture download!'%count
            return True
        else:
            print 'urlopen failed'
            return False
	
    def downloadimg_(self):
        print 'saving picture...',
        try:
            imgpath = self.basepath + self.imgurl
            imgpath = imgpath.encode('gbk')
            #pdb.set_trace()
            img = urllib2.urlopen(imgpath).read()
            file = open(self.filepath,'wb')
            file.write(img)

            #txtfile
            if os.path.exists(self.txtpath):
                os.remove(self.txtpath)
            #txtfile = open(self.txtpath, 'wb')
            #txtfile.write(self.copyright)
            txtfile = codecs.open(self.txtpath, 'w', 'GBK')
            txtfile.write(self.copyright)
        finally:
            file.close()
            txtfile.close()
        
        print 'done'

    def save2bmp(self):
        if os.path.exists(self.filepath):
            jpgimg = cv2.imread(self.filepath)
            
            #jpgimg = self.ft.draw_text(jpgimg, (1800, 1000), self.copyright,  15, (138,138,138))
            
            cv2.imwrite(self.bmppath,jpgimg)
            os.remove(self.filepath)
            print 'jpg changed to bmp'
			
class Setimage():
	def __init__(self):
		self.bmppath = 'G:\\bingImage\\today.bmp'
		self.workpath = 'F:\\Projects\\bing\\Debug'
		self.exepath = 'F:\\Projects\\bing\\Debug\\bing.exe'
	
	def seting(self):
		flag = False
		try:
			handle = win32process.CreateProcess(self.exepath, '', None, None, 0, 
							win32process.CREATE_NO_WINDOW, 
							None, 
							self.workpath, 
							win32process.STARTUPINFO())
			flag = True
		except Exception, e:
			print 'Create win32 process failed!'
			handle = None
			flag = False
		
		while flag:
			rc = win32event.WaitForSingleObject(handle[0], 1000)
			if rc == win32event.WAIT_OBJECT_0:
				flag = False
		
		print 'done!'

if __name__ == '__main__':
    getimg = Getimage()
    getimg.crawb()
    '''
    if getimg.downloadimg():
		getimg.save2bmp()
		setimg = Setimage()
		setimg.seting()
    '''
    getimg.downloadimg_()
    getimg.save2bmp()
    setimg = Setimage()
    setimg.seting()