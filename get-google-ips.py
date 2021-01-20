import requests
import json
import codecs
from IPy import IPSet, IP

r = requests.get('https://www.gstatic.com/ipranges/goog.json')
data = []
data.append(json.loads(r.text))

file_object = codecs.open('google-ip-ranges-'+data[0]['creationTime'][0:10]+'.txt', 'w' ,"utf-8")

for ip_ranges in data[0]['prefixes']:
  #print(ip_ranges['ipv4Prefix'])
  try:
    file_object.write('/ip fir add add add='+ip_ranges['ipv4Prefix']+' comment="GOOGLE LLC '+data[0]['creationTime'][0:10]+'" list=dst-use-vpn'+"\r\n")
  except:
    try:
      file_object.write('/ipv6 fir add add add='+ip_ranges['ipv6Prefix']+' comment="GOOGLE LLC '+data[0]['creationTime'][0:10]+'" list=dst-use-vpn'+"\r\n")
    except:
      pass

r = requests.get('https://www.gstatic.com/ipranges/cloud.json')
data = []
data.append(json.loads(r.text))

ret = IPSet()
for ip_ranges in data[0]['prefixes']:
  try:
    curip=ip_ranges['ipv4Prefix']
    ret.add(IP(curip, make_net = True))
  except:
    try:
      file_object.write('/ipv6 fir add add add='+ip_ranges['ipv6Prefix']+' comment="GOOGLE Cloud '+data[0]['creationTime'][0:10]+'" list=dst-use-vpn'+"\r\n")
    except:
      pass

for ip_ranges in ret:
  try:
    file_object.write('/ip fir add add add='+ip_ranges.strNormal()+' comment="GOOGLE Cloud '+data[0]['creationTime'][0:10]+'" list=dst-use-vpn'+"\r\n")
  except:
    # do nothing
    pass

file_object.close()
print('success! file '+'google-ip-ranges-'+data[0]['creationTime'][0:10]+'.txt')
