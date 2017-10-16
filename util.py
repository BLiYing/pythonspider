#!/usr/bin/python
# -*- coding: UTF-8 -*-
import gzip
from io import StringIO

import zlib

import datetime

def writeerrorlog(searchid = 0,reasonstr = '',url= '',code = 0):
    flog = open('logerror.txt', 'a+')
    timeerror = datetime.datetime.now()
    flog.write('\n')
    flog.write('\n')
    flog.write('----------------------')
    flog.write('\n')
    flog.write('Time:'+str(timeerror))
    flog.write('\n')
    flog.write(u'MID:'+str(searchid))
    flog.write('\n')
    flog.write('Error:' + reasonstr)
    flog.write('\n')
    flog.write('url:' + url)
    flog.write('\n')
    flog.write('Code:'+str(code))

def writeMIDTOtxt(searchid):
    flog = open('MIDLIST.txt', 'a+')
    flog.write('\n')
    flog.write(str(searchid))

def writeTheLastMIDTOtxt(lastsearchid):
    flog = open('LASTMID.txt', 'w+')
    flog.write('\n')
    flog.write(str(lastsearchid))

def getTheLastMID():
    lastmidstr = open('LASTMID.txt').read()
    if lastmidstr and lastmidstr != '\n':
        return lastmidstr
    else:
        return '0'


def ggzip(data):
    buf = StringIO(data)
    f = gzip.GzipFile(fileobj=buf)
    return f.read()


def deflate(data):
    try:
        return zlib.decompress(data, -zlib.MAX_WBITS)
    except zlib.error:
        return zlib.decompress(data)