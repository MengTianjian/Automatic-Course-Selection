import urllib
import urllib2
import cookielib
import os
import Image
import StringIO

def binary(img):
    img = Image.open(StringIO.StringIO(img))
    img = img.convert("RGBA")
    pixdata = img.load()
    for y in xrange(img.size[1]):
        for x in xrange(img.size[0]):
            if pixdata[x, y][0] < 90:
                pixdata[x, y] = (0, 0, 0, 255)
    for y in xrange(img.size[1]):
        for x in xrange(img.size[0]):
            if pixdata[x, y][1] < 136:
                pixdata[x, y] = (0, 0, 0, 255)
    for y in xrange(img.size[1]):
        for x in xrange(img.size[0]):
            if pixdata[x, y][2] > 0:
                pixdata[x, y] = (255, 255, 255, 255)
    return img

nume = 0

def division(img):
    global nume
    font = []
    pixdata = img.load()
    a = []
    b = []
    for x in xrange(img.size[0]):
        for y in xrange(img.size[1]):
            if pixdata[x, y][0] == 0:
                a.append(x)
                break
    b.append(a[0]-1)
    for i in range(len(a)-1):
        if a[i+1]-a[i] > 1:
            b.append(a[i]+2)
            b.append(a[i+1]-1)
    b.append(a[len(a)-1]+1)
    i = 0
    if len(b) == 8:
        while i <= 6:
            temp = img.crop((b[i], 0, b[i+1], 20))
            i += 2
            nume += 1
            font.append(temp)
    return font



def recognize(img):
    fontMods = {}
    for i in range(10):
        fontMods[str(i)] = Image.open("./font2/%d.gif"%i)
    Upper = ['A','B','C','D','E','F','G','H','J','K','L','M','N','P','Q','R','S','T','U','V','W','X','Y','Z']
    Lower = ['a','b','d','e','f','g','h','j','n','q','r','t','w','x','y']
    for i in Upper:
        fontMods[i] = Image.open("./font2/%s.gif"%i)
    for i in Lower:
        fontMods[i] = Image.open("./font2/%s1.gif"%i)
        result = ""
    font = division(img)
    for i in font:
        target = i
        pixdata = target.load()
        points = []
        for mod in fontMods.keys():
            diffs = 0
            if target.size[0] > fontMods.get(mod).size[0]:
                r = fontMods.get(mod).size[0]
            else:
                r = target.size[0]
            for x in range(r):
                for y in xrange(target.size[1]):
                    if pixdata[x, y] != fontMods.get(mod).convert("RGBA").load()[x,y]:
                        diffs += 1
            points.append((diffs, mod))
        points.sort()
        result += points[0][1]
    return result

if __name__ == '__main__':
    print '//  Created by Tianjian Meng on 6/7/16.'
    print '//  Copyright @ 2016 BJTU. All rights reserved.'
    zjh=raw_input('Please Input Student ID:')
    mm=raw_input('Please Input Password:')
    cookie_support=urllib2.HTTPCookieProcessor(cookielib.CookieJar())
    opener=urllib2.build_opener(cookie_support)
    urllib2.install_opener(opener)
    header={
        'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; WOW64; Trident/6.0)',
        'Connection': 'Keep-Alive'
        }
    yzmrequest=urllib2.Request(url='http://121.194.57.131/validateCodeAction.do',headers=header)
    login=-1
    while (login==-1):
        while True:
            content=urllib2.urlopen(yzmrequest).read()
            img = binary(content)
            if (len(division(img))==4):
                result = recognize(img)
                break
        loginform={
            'zjh1': '',
            'tips': '',
            '1x': '',
            'evalue': '',
            'eflag': '',
            'fs': '',
            'dzslh': '',
            'zjh': zjh,
            'mm': mm,
            'v_yzm' : result
            }
        loginform_data=urllib.urlencode(loginform)
        loginrequest=urllib2.Request('http://121.194.57.131/loginAction.do',loginform_data,headers=header)
        loginresponse=urllib2.urlopen(loginrequest)
        login=loginresponse.read().find("www.w3.org")
    print 'Successful Login!'
    while True:
        kch=raw_input('Please Input Course ID(XXXXXXX):')
        kxh=raw_input('Please Input Course No(XX):')
        page=raw_input('Please Input Page Number:')
        re=urllib2.Request(url="http://121.194.57.131/rxkAction.do?actionType=2&cxType=kch&pageNumber=-1&&kch=&kxh=&rxklb=&xsyyl=&krlPxfs=desc&kchPxfs=asc",headers=header)
        res=urllib2.urlopen(re)
        re2=urllib2.Request(url="http://121.194.57.131/rxkAction.do?actionType=4&pageNumber="+page,headers=header)
        res2=urllib2.urlopen(re2)
        yzmrequest=urllib2.Request(url='http://121.194.57.131/validateCodeAction.do?random=random=',headers=header)
        i=1
        header={
            'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; WOW64; Trident/6.0)',
            'Connection': 'Keep-Alive',
            'Referer': 'http://121.194.57.131/rxkAction.do?actionType=4&pageNumber='+page
            }
        pick=-1
        while (pick==-1):
            while True:
                content=urllib2.urlopen(yzmrequest).read()
                img=binary(content)
                if (len(division(img))==4):
                    result = recognize(img)
                    break
            pickform={
                'ifraType': 'wct',
                'v_yzm': result,
                'bclx': 'rxk',
                'krlPxfs': 'asc',
                'kchPxfs': 'desc',
                'pageNumber': page,
                'pageNo': '',
                'kcId': kch+'_'+kxh
                }
            pickform_data=urllib.urlencode(pickform)
            pickrequest=urllib2.Request('http://121.194.57.131/rxkBtxAction.do?actionType=3',pickform_data,headers=header)
            pickresponse=urllib2.urlopen(pickrequest)
            pick=pickresponse.read().find("btnReturn")
            print 'No.'+str(i)+' try'
            i+=1
        print 'Done.'
