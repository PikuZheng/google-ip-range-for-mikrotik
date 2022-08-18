import requests
import json
import codecs
from IPy import IPSet, IP
import sys

data = []
r = requests.get('https://www.gstatic.com/ipranges/goog.json')
data.append(json.loads(r.text))
r = requests.get('https://www.gstatic.com/ipranges/cloud.json')
data.append(json.loads(r.text))

file_object = codecs.open('google-ip-ranges.txt', 'w' ,"utf-8")
file_object.write('/ip fir add remove [/ip fir add find comment~"^GOOGLE LLC .*"]'+"\r\n")
file_object.write('/ipv6 fir add remove [/ip fir add find comment~"^GOOGLE LLC .*"]'+"\r\n")

ipset = IPSet()
for dat in data:
  for ip_ranges in dat['prefixes']:
    try:
      ipset.add(IP(ip_ranges['ipv4Prefix'], make_net = True))
    except:
      try:
        ipset.add(IP(ip_ranges['ipv6Prefix'], make_net = True))
      except:
        pass

for ip_ranges in ipset:
  try:
    if ip_ranges.version() == 4:
      file_object.write(':do { /ip fir add add add='+ip_ranges.strNormal()+' comment="GOOGLE LLC '+data[0]['creationTime'][0:10]+'" list=dst-use-vpn'+" } on-error={}\r\n")
    else:
      file_object.write(':do { /ipv6 fir add add add='+ip_ranges.strNormal()+' comment="GOOGLE LLC '+data[0]['creationTime'][0:10]+'" list=dst-use-vpn'+" } on-error={}\r\n")
  except:
    pass

file_object.close()
print('success! file '+'google-ip-ranges-simple-'+data[0]['creationTime'][0:10]+'.txt')
