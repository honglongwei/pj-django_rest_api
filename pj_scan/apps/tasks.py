#_*_ coding:utf-8 _*_

import urllib2
import sys
from celery import task
from libs.nmap import nmap
from .models import BaseMsg, SrvMsg

@task()
def startScan(ip, port, id):
    IP = BaseMsg.objects.get(id=int(id))
    scanner = nmap.PortScanner()
    req = scanner.scan(hosts=str(ip), arguments='-sV')
    det = req['scan'][str(ip)]['tcp']
    ct = []
    for k, v in det.items():
        ct.append(k)
        bb = SrvMsg(dip=IP, midport=k, midtype=v['product'], midversion=v['version'])
        bb.save()
        if 'sql' in v['product'].lower():
            IP.dbtype = v['product']
            IP.dbversion = v['version']
            IP.save()
    title_str, html = '', ''
    try:
        if port == 443:
            info = urllib2.urlopen("https://%s:%s" % (ip, port), timeout=2)
        else:
            info = urllib2.urlopen("http://%s:%s" % (ip, port), timeout=2)
        html = info.read()
        header = info.headers
    except urllib2.HTTPError, e:
        html = e.read()
        header = e.headers
    except:
        pass
    try:
        if not header:pass
        if 'Content-Encoding' in header and 'gzip' in header['Content-Encoding']: 
            html_data = StringIO.StringIO(html)
            gz = gzip.GzipFile(fileobj=html_data)
            html = gz.read()
        try:
            html_code = get_code(header, html).strip()
            if html_code and len(html_code) < 12:
                html = html.decode(html_code).encode('utf-8')
        except: pass
        try:
            title = re.search(r'<title>(.*?)</title>', html, flags=re.I | re.M)
            if title: title_str = title.group(1)
        except: pass
        try:
            banner = header
        except:
            print 3
        ret = {}
        if banner['Server']:
            dweb = banner['Server'].split(" ")
            daset = dweb[0].split("/")
            try:
                if banner['X-Powered-By']:
                    devla = banner['X-Powered-By']
                    if len(devla.split("/")) <= 1:
                        ret['devla'] = devla
                        ret['langv'] = ''
                    elif len(devla.split("/")) > 1:
                        ret['devla'] = devla.split("/")[0]
                        ret['langv'] = devla.split("/")[1]
                    else:
                        ret['devla'] = ''
                        ret['langv'] = ''
                else:
                    devla = ''
                ret['web'] = daset[0]
                ret['version'] = daset[1]
                ret['os'] = str(dweb[1]).strip('(|)')
            except:
                ret['web'] = daset[0]
                try:
                    ret['version'] = daset[1]
                except:
                    ret['version'] = ''
                ret['os'] = ''
                ret['devla'] = ''
        else:
            ret = {'web':'', 'version':'', 'os':'', 'devla':'', 'langv':''} 
        aa = BaseMsg.objects.get(id=id)
        aa.s_count = str(len(ct))
        aa.devlang = ret['devla']
        aa.langver = ret['langv']
        aa.webtype = ret['web']
        aa.webversion = ret['version']
        aa.osinfo = ret['os']
        aa.save()
    except:
        aa = BaseMsg.objects.get(id=id)
        aa.s_count = str(len(ct))
        aa.save()
    ty = BaseMsg.objects.get(id=id)
    if str(ty.webtype) == '':
        if port in ct:
            ty.webtype = det[int(port)]['product'] 
            ty.webversion = det[int(port)]['version']
            ty.save()
        else:
            pass
    else:
        pass    
    return banner
