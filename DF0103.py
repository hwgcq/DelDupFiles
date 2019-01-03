#/usr/bin/env python
#DF0103.py
#Delete duplicate files.
#2019-01-03 17:20 微调，50k以下文件不处理
#2018-12-15 21:37 搞定
#2018-12-15 18:41 微调显示，显示文件尺寸，处理速度
	#简化工作方式：以后都copy该文件到需要的目录下运行即可。不去选Dir了。
#2018-12-13 11:34 for termux
#2018-08-25 16:15 hwg
#-*- coding:utf-8 -*-

import os,sys
from datetime import datetime
tfmt='%Y-%m-%d %H:%M:%S'

class Logger:
    def __init__(self, filename='DelDupFiles.log'):
        self.terminal = sys.stdout
        self.log = open(filename, 'w')
    def __del__(self):
        self.log.close()
    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)
    def flush():
        pass

def GetDirS(dir):
    from os.path import join, getsize
    N,S = 0,0
    for root, dirs, files in os.walk(dir):
        N += len(files)
        S += sum([getsize(join(root, name)) for name in files])
    return N,S
 
def HashF(filefullpath,block=2**20):
    from hashlib import sha256 as hm
    import sys
    f=open(filefullpath,'rb')
    h=hm()
    i=0
    while True:
        i+=1
        if i>=10:
            print('.',end='')
            i=0
        data=f.read(block)
        if not data:
            break
        h.update(data)
    f.close()
    return h.hexdigest()

def get_key (dic, value):
    return [k for k, v in dic.items() if v == value]
 
def DelDupF(Dir,minSize=50e3):
    N,S=GetDirS(Dir)
    dic={}
    n1,s1=0,0
    n2,s2=0,0
    for root, subdirs, files in os.walk(Dir):
        for file in files:
            ff = os.path.join(root,file)
            n1+=1
            Size=os.path.getsize(ff)
            s1+=Size
            rf=os.path.relpath(ff,Dir)
            print (rf,end='')
            h=HashF(ff)
            print('\t'+h+'\t'+'{:,}'.format(Size)+'\t%.1f' % (s1/S*100.0)+'%',end='')
            if os.path.getsize(ff) < minSize:print();continue
            if h in dic.keys():
                n2+=1
                s2+=os.path.getsize(ff)
                print('\tDelete!')
                os.remove(ff);
                f=open(ff+'.hash','w');f.write(dic[h]+'\t'+h+'\t'+'{:,}'.format(Size)+' B');f.close()
            else:
                dic[h]=rf
                print()
    return dic,N,S,n2,s2

stdout_bk = sys.stdout

Dir=os.getcwd()
t1=datetime.now();
sys.stdout = Logger('DF'+t1.strftime('%y%m%d-%H%M')+'.log')
t1=datetime.now();print('Begin '+ t1.strftime(tfmt));print(Dir+'\n')
print('File\tSHA-256\tSize\tProgress')
dic,N,S,n2,s2=DelDupF(Dir,minSize=50e3)
t2=datetime.now();print('\nEnd '+ t1.strftime(tfmt));print(Dir+'\n')
print('Total\t' +'{:,}'.format(N) +' File(s)\t'+'{:,}'.format(S) +'\tB')
print('Del\t'+'{:,}'.format(n2)+' File(s)\t'+'{:,}'.format(s2)+'\tB')
dt=t2-t1
print('Time: ' + str(dt))
if dt:speed=S/(dt.seconds+dt.microseconds/1e6)
else:speed=0
print('Speed: '+'{:,}'.format(int(speed))+' B/s')

sys.stdout=stdout_bk
