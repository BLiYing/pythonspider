#!/usr/bin/python3
import json
import os
import urllib.request, urllib.parse, urllib.error
import http.cookiejar

import zlib
from bs4 import BeautifulSoup
from html.parser import HTMLParser

import re
import datetime
import saveinExcel
from util import ggzip, deflate, writeerrorlog, writeMIDTOtxt, writeTheLastMIDTOtxt, getTheLastMID

LOGIN_URL = 'https://metlin.scripps.edu/lib/json/auth.php'
get_url = 'https://metlin.scripps.edu/landing_page.php?pgcontent=advanced_search'  # 利用cookie请求访问另一个网址

user_agent = r'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'

headers = {'User-Agent': user_agent,
           'Host': 'metlin.scripps.edu',
           'Referer': 'https://metlin.scripps.edu/landing_page.php?pgcontent=mainPage',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
           'Connection': 'keep-alive',
           'Accept-Language': 'zh-CN,zh;q=0.8',
           'Accept-Encoding': 'gzip, deflate, br',
           }
# cookie
cookie_filename = 'other_cookie_jar.txt'
# opener = ''
# 超时时间
timeout = 30
# list存放需要的数据
oneData = {}
##终止与此
bianhaoID = 65000 
# 搜索关键词MID
MID = 60000 
csvFile = 'american.csv'
# cookie是否有效
FLAGCOOKIE = False
# 每次开始插入时的id
newIndex = 0


def freshCookie():
    # global opener
    print(u'\n---cookie失效,需要更新---\n')
    login()
    get_cookie = getCookie(cookie_filename)
    openernew = getOpener(get_cookie)
    return openernew


def getCookie(cookie_filename):
    cookie = http.cookiejar.MozillaCookieJar(cookie_filename)
    cookie.load(cookie_filename, ignore_discard=True, ignore_expires=True)
    # print(cookie)
    return cookie


def getOpener(m_cookie):
    global FLAGCOOKIE
    handler = urllib.request.HTTPCookieProcessor(m_cookie)
    opener = urllib.request.build_opener(handler)
    FLAGCOOKIE = True
    return opener


def getBangzhuangTu(url, mopener):
    global FLAGCOOKIE
    global MID
    print('正在获取棒状图.......')

    soup = getsoup(url, mopener)
    if soup:
        soup.prettify('utf-8')
        new_cont = soup.find_all('script')
        index_script = 0
        for child in new_cont:
            if (index_script == 4):
                # print(child)
                # print(type(child))
                # print(child.string)
                resultstr = child.string
                startstr = 'series:'
                endstr = ']}]'
                indexstart = resultstr.find(startstr)
                indexend = resultstr.find(endstr)
                # print(indexstart)
                # print(indexend)
                substr = resultstr[int(indexstart) + len(startstr):int(indexend)]
                substr += endstr
                substr = substr.replace('&nbsp;', '').replace(' ', '').replace('quotes', '')
                # print(substr)
                test = re.sub('\'', '', substr)
                # print(test)
                test = test.replace('name:', '"name":"') \
                    .replace(',data:', '","data":').replace('x:', '"x":"').replace(',y:', '","y":"') \
                    .replace(',fragment:', '","fragment":')
                # print(type(test))
                print('---棒状图结果集---')
                # print(test)
                print('---棒状图结果集---')
                test = test.replace('},]', '"}]')
                liststr = json.loads(test)
                # 循环插入数据，依据每个能量值不同，共8个能量值
                for item in liststr:
                    modeandenegy = item['name']
                    gcollisionenergy_value = modeandenegy[3:]
                    gh_mode = modeandenegy[0:3]
                    datalist = item['data']
                    rows = []
                    rows.append(oneData[saveinExcel.ametlin])
                    rows.append(oneData[saveinExcel.blmass])
                    rows.append(oneData[saveinExcel.ename])
                    rows.append(oneData[saveinExcel.hformula])
                    rows.append(oneData[saveinExcel.fgcas])
                    rows.append(oneData[saveinExcel.kegg])
                    rows.append(oneData[saveinExcel.gxms])
                    rows.append(gcollisionenergy_value)
                    rows.append(gh_mode)
                    for datachild in datalist:
                        datachildx = datachild['x']
                        datachildy = datachild['y']
                        rows.append(datachildx)
                        rows.append(datachildy)
                    saveinExcel.saverow(dict_writer, rows)
                    print('---save success---')

            index_script += 1


def getsoup(url_search, mopener):
    global FLAGCOOKIE
    global MID
    get_request = urllib.request.Request(url_search, headers=headers)
    try:
        get_response = mopener.open(get_request, timeout=timeout)
        content = get_response.read()
        text = ''
        encoding = get_response.info().get('Content-Encoding')
        if encoding == 'gzip' and len(content) > 0:
            decompressed_data = zlib.decompress(content, 16 + zlib.MAX_WBITS)
            # print(type(decompressed_data))
            text = decompressed_data.decode('utf8')
        # print('------------')
        # print(text)
        # print('------------')
        if text and get_response and get_response.status == 200:
            soup = BeautifulSoup(text, "html.parser")
            return soup
    except urllib.error.HTTPError as e:
        import time
        time.sleep(10)
        print(u'---search搜索httperror---')
        writeerrorlog(str(MID)+'\n'+url_search, str(e.reason), str(e.geturl()), e.code)
        print(e.code, ':', e.reason)
        print(u'---search搜索httperror---')
        FLAGCOOKIE = False
        openernew = freshCookie()
        searchGo(openernew)

    except urllib.error.URLError as e:
        import time
        time.sleep(10)
        print(e.reason)
        writeerrorlog(str(MID)+'\n'+url_search, str(e.reason), '', 0)
        FLAGCOOKIE = False
        openernew = freshCookie()
        searchGo(openernew)
    except Exception as e:
        import time
        time.sleep(10)
        writeerrorlog(str(MID), str(e), '', 1111)
        openernew = freshCookie()
        searchGo(openernew)

# 先搜索
def search(mid, opener):
    global FLAGCOOKIE
    global MID
    print('\n正在搜索MID %s.......' % mid)
    # 最后一次的mid写入
    writeTheLastMIDTOtxt(mid)
    url_search = 'https://metlin.scripps.edu/advanced_search_result.php?molid=%s&mass_min=&mass_max=&name=&formula=&cas=&kegg=&smilefile=&msmspeaks_min=&AminoAcid=add&drug=add&toxinEPA=add&smilesExactMatchCheckBox=false&nameExactMatchCheckBox=false' % mid

    soup = getsoup(url_search,opener)
    if soup:
        linkTag = soup.find_all('tr')
        # print(linkTag)
        print('---成功搜索到关键字信息---')
        oneData[saveinExcel.ametlin] = MID
        for child_tr in linkTag:
            # print(child_tr)
            if 'td' in str(child_tr):
                linkTags = child_tr.find_all('td')
                if len(linkTag) > 0:
                    n = 0
                    for childtd in linkTags:
                        # print(childtd.string)
                        if n == 0:
                            mass = childtd.string
                            print(mass)
                            oneData[saveinExcel.blmass] = str(mass)
                        elif n == 1:
                            name = childtd.string
                            # print(name)
                            oneData[saveinExcel.ename] = str(name)
                        elif n == 2:
                            formula = childtd.string
                            # print(formula)
                            oneData[saveinExcel.hformula] = str(formula)
                        elif n == 3:
                            cas = childtd.string
                            # print(cas)
                            oneData[saveinExcel.fgcas] = str(cas)
                        elif n == 4:
                            kegg = childtd.string
                            # print(kegg)
                            oneData[saveinExcel.kegg] = str(kegg)
                        elif n == 5 and 'href' in str(childtd):
                            try:
                                aTag = childtd.a
                            except AttributeError as e:
                                print(e.args)
                                print('Tag was not found')
                            else:
                                if aTag:
                                    href = aTag['href']
                                    print(href)
                                    host = 'https://metlin.scripps.edu/'
                                    experimental = 'experimental'
                                    if experimental in href:
                                        host = host + href
                                        # print(host)
                                        oneData[saveinExcel.gxms] = experimental
                                        if FLAGCOOKIE:
                                            writeMIDTOtxt(mid)
                                            getBangzhuangTu(host, opener)
                                else:
                                    print('aTag was not found')
                        n += 1
    else:
        print('---返回html为空---')


def checkCookieIsUseful():
    headers = {'User-Agent': user_agent,
               'Host': 'metlin.scripps.edu',
               'Referer': 'https://metlin.scripps.edu/landing_page.php?pgcontent=mainPage',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
               'Connection': 'keep-alive',
               'Accept-Encoding': 'gzip, deflate, br',
               }
    cookie = getCookie(cookie_filename)
    handler = urllib.request.HTTPCookieProcessor(cookie)
    opener = urllib.request.build_opener(handler)
    get_request = urllib.request.Request(get_url, headers=headers)
    get_response = opener.open(get_request, timeout=timeout)

    if get_response.status == 200:
        print('---cookie有效---')
        return True
    else:
        return False


def login():
    global FLAGCOOKIE
    global MID
    print('---------is logining................')
    # values = {'user': 'tjuciliying@163.com', 'passwo#rd': '198926'}
    values = {'user': 'scj566286@163.com', 'password': 'scj566286@163.com'}
    postdata = urllib.parse.urlencode(values).encode()
    headers = {'User-Agent': user_agent}

    cookie_jar = http.cookiejar.MozillaCookieJar(cookie_filename)
    handler = urllib.request.HTTPCookieProcessor(cookie_jar)
    opener = urllib.request.build_opener(handler)

    request = urllib.request.Request(LOGIN_URL, postdata, headers)
    try:
        response = opener.open(request, timeout=timeout)
        if response and response.status == 200:
            print(u'---登录成功---')
            # print(response.read().decode())
    except urllib.error.HTTPError as e:
        print(u'---login HTTPError---')
        writeerrorlog(str(MID) + '\n', str(e.reason), str(e.geturl()), e.code)
        print(e.code, ':', e.reason)
        print(u'---login HTTPError---')
        FLAGCOOKIE = False
        openernew = freshCookie()
        searchGo(openernew)

    except urllib.error.URLError as e:
        import time
        time.sleep(10)
        print(u'---login URLError---')
        print(e.reason)
        writeerrorlog(str(MID) + '\n', str(e.reason), '', 2222)
        FLAGCOOKIE = False
        openernew = freshCookie()
        searchGo(openernew)
    except Exception as e:
        import time
        time.sleep(10)
        writeerrorlog(str(MID), str(e), '', 1111)
        FLAGCOOKIE = False
        openernew = freshCookie()
        searchGo(openernew)
    cookie_jar.save(ignore_discard=True, ignore_expires=True)  # 保存cookie到cookie.txt中
    # for item in cookie_jar:
    #     print('Name = ' + item.name)
    #     print('Value = ' + item.value)


# 执行搜索
def searchGo(opener):
    # global freshIndex
    global oneData
    global FLAGCOOKIE
    global MID

    # freshIndex = newIndex
    # noinspection PyRedundantParentheses
    while ((MID <= bianhaoID) and FLAGCOOKIE):
        # 初始化数据
        # rows = []
        import time
        time.sleep(1)
        oneData = {
            saveinExcel.ametlin: '', saveinExcel.blmass: '', saveinExcel.ename: '',
            saveinExcel.hformula: '', saveinExcel.fgcas: '', saveinExcel.kegg: '', saveinExcel.gxms: ''
        }
        if MID % 100 == 0:
            FLAGCOOKIE = False
            opener = freshCookie()
        if FLAGCOOKIE:
            search(str(MID), opener)
            MID += 1


if __name__ == "__main__":
    # 程序开始时间
    starttime = datetime.datetime.now()
    # 创建excel表格
    dict_writer = saveinExcel.creatCvs(csvFile)
    # 登录
    login()
    # 获取网络句柄
    get_cookie = getCookie(cookie_filename)
    opener = getOpener(get_cookie)
    lastmid = int(getTheLastMID())
    if MID < lastmid:
        newIndex = lastmid
    if newIndex < MID:
        newIndex = MID
    print('从%d开始插入' % newIndex)
    MID = newIndex
    searchGo(opener)
    endtime = datetime.datetime.now()
    usetime = u'耗时' + (endtime - starttime).seconds.__str__() + 's'
    print(usetime)
