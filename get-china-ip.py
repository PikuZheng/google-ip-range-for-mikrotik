import requests
import codecs
from IPy import IPSet, IP
from contextlib import closing
import math

ipset = IPSet()
str_update = ""

print ("read ip list from apnic...", end="")
with closing(requests.get('http://ftp.apnic.net/stats/apnic/delegated-apnic-latest', stream=True)) as r:
  r.encoding='utf-8'
  content_size = int(r.headers['content-length'])
  response = r.iter_lines()
  total=0
  for gen_lines in response:
    total += len(gen_lines)
    print("\rread ip list from apnic...%0.1f%%" % (float(total/content_size) * 100) , end='')
    try:
      l=str(gen_lines).split("|")
      if (l[1]=="CN" and l[2][0:2]=="ip"):
        ipset.add(IP( l[3]+"/"+str(int(32-math.log(int(l[4]))/math.log(2))), make_net = True ))
      elif (l[1]=="apnic"):
        str_update=l[2]
    except:
      pass
print ("\b\b\b\b\b\b...done")

print ("translate ip to rsc...", end="")
with codecs.open('china-ip-ranges-ipv4-'+str_update+'.txt', 'w' ,"utf-8") as output_ipv4, codecs.open('china-ip-ranges-ipv6-'+str_update+'.txt', 'w' ,"utf-8") as output_ipv6:
  for ip_range in ipset:
    try:
      if ip_range.version() == 4:
        print(ip_range.strNormal())
        output_ipv4.write('/ip fir add add add='+ip_range.strNormal()+' comment="China'+str_update+'" list=dst-use-no-vpn'+"\r\n")
      else:
        output_ipv6.write('/ipv6 fir add add add='+ip_range.strNormal()+' comment="China'+str_update+'" list=dst-use-no-vpn'+"\r\n")
    except:
      pass
print ("done")
