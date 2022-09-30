import requests
import codecs
from contextlib import closing
import datetime

ipset = IPSet()
str_update = datetime.datetime.now().strftime('%Y-%m-%d')

print ("read ip list from github...", end="")
with closing(requests.get('https://github.com/gaoyifan/china-operator-ip/raw/ip-lists/china.txt', stream=True)) as r, codecs.open('china-ip-ranges-ipv4.txt', 'w' ,"utf-8") as output_ipv4:
  r.encoding='utf-8'
  response = r.iter_lines()
  output_ipv4.write('/ip fir add remove [/ip fir add find comment~"^China20[0-9]*"]'+"\r\n")
  for ip_range in response:
    try:
#        print(ip_range.strNormal())
        output_ipv4.write(':do { /ip fir add add add='+ip_range.decode()+' comment="China'+str_update+'" list=dst-use-no-vpn'+" } on-error={}\r\n")
    except:
      pass
print ("done")

with closing(requests.get('https://github.com/gaoyifan/china-operator-ip/raw/ip-lists/china6.txt', stream=True)) as r, codecs.open('china-ip-ranges-ipv6.txt', 'w' ,"utf-8") as output_ipv6:
  r.encoding='utf-8'
  response = r.iter_lines()
  output_ipv6.write('/ipv6 fir add remove [/ipv6 fir add find comment~"^China20[0-9]*"]'+"\r\n")
  for ip_range in response:
    try:
        output_ipv6.write('/ipv6 fir add add add='+ip_range.strNormal()+' comment="China'+str_update+'" list=dst-use-no-vpn'+"\r\n")
    except:
      pass
print ("done")
