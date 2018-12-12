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
from putChineseText import put_chinese_text
import pdb

bmppath = '/home/mayuan/PROJECTS/Bing_wallpaper/today/today.bmp'

class Getimage(object):
    def __init__(self):
        self.filepath = '/home/mayuan/PROJECTS/Bing_wallpaper/today.jpg'
        self.txtpath = '/home/mayuan/PROJECTS/Bing_wallpaper/today.txt'
        self.bmppath = bmppath
        self.basepath = 'http://www.bing.com'
        self.imgurl = 0
        
        self.ft = put_chinese_text('/home/mayuan/PROJECTS/Bing_wallpaper/wqy-zenhei.ttc')

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
            '''
            #txtfile
            if os.path.exists(self.txtpath):
                os.remove(self.txtpath)
            #txtfile = open(self.txtpath, 'wb')
            #txtfile.write(self.copyright)
            txtfile = codecs.open(self.txtpath, 'w', 'GBK')
            txtfile.write(self.copyright)
            '''
        finally:
            file.close()
            #txtfile.close()
        
        print 'done'

    def save2bmp(self):
        if os.path.exists(self.filepath):
            jpgimg = cv2.imread(self.filepath)
            jpgimg = self.ft.draw_text(jpgimg, (1450, 1000), self.copyright, 20, (250, 250, 250))
            
            cv2.imwrite(self.bmppath,jpgimg)
            os.remove(self.filepath)
            print 'jpg changed to bmp'

class Setimage():
    def __init__(self):
        self.bmppath = '/home/mayuan/PROJECTS/Bing_wallpaper/today/today.bmp'
        self.cmd = 'gsettings set org.gnome.desktop.background picture-uri \"file:'
        self.cmd += self.bmppath + '\"'

    def setimg(self):
        print 'Setting wallpaper...'
        try:
            os.system(self.cmd)
        except Exception, e:
            print 'Set wallpaper failed!'

        print 'done!'

if __name__ == '__main__':
    getimg = Getimage()
    getimg.crawb()
    getimg.downloadimg_()
    getimg.save2bmp()
    
    setimg = Setimage()
    setimg.setimg()
