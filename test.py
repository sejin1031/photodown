from bs4 import BeautifulSoup
import re
import requests
import urllib
from urllib.request import urlopen


headers = {'Content-Type': 'application/json; charset=utf-8',
    "User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/74.0.3729.169 Chrome/74.0.3729.169 Safari/537.36"}

r = requests.get("https://gall.dcinside.com/mgallery/board/lists/?id=fromis&sort_type=N&search_head=20&page=1", headers = headers)
bsObject = BeautifulSoup(r.text, "html.parser")

links = []
links2 = []
for link in bsObject.find_all('td',{'class':'gall_tit ub-word'}):
    for link2 in link.find_all('a'):
        links.append(link2.get('href'))

for link in links:
    if 'http' in link:
        links2.append(link)

for link in links2:
    