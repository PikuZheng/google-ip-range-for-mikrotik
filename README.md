# google-ip-range-for-mikrotik
get ip ranges from google and import to mikrotik

to automated update in Mikrotik：

add a scheduler with
```
/tool fetch url="https://raw.githubusercontent.com/PikuZheng/google-ip-range-for-mikrotik/main/china-ip-ranges-ipv4.txt"
/import file="china-ip-ranges-ipv4.txt"
```
