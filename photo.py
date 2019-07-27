from bs4 import BeautifulSoup
import re
import requests
import urllib
from urllib.request import urlopen

def img_link(soup, name_list, url):
    opener = urllib.request.build_opener()
    opener.addheaders = [("Referer", url)]
    urllib.request.install_opener(opener)
    div_class = soup.find("div", class_="writing_view_box")
    img_class = div_class.find_all("img")
    for i in range(0, len(img_class), 1):
        string_img_url = str(img_class[i])
        tmp_start_urlPoint = string_img_url.find("src=")
        tmp_end_urlPoint = string_img_url.find("style=")
        string_img_url = string_img_url[tmp_start_urlPoint + 5:tmp_end_urlPoint-2]
        string_img_url = string_img_url.replace("amp;", "")
        urllib.request.urlretrieve(string_img_url, "./" + name_list[i])

def name(soup, name_list):
    ul_class = soup.find("ul", class_="appending_file")
    a_tags = ul_class.find_all("a")
    for i in range(0, len(a_tags), 1):
        string_name = str(a_tags[i])
        tmp_start_namePoint = string_name.find(">")
        tmp_end_namePoint = string_name.find("</a>")
        string_name = string_name[tmp_start_namePoint + 1 : tmp_end_namePoint]
        name_list.append(string_name)
    name_list.sort()

def debuging_request(r):
    f = open("debuger.txt", mode="wt", encoding="utf-8")
    f.write(r)
    f.close()

if __name__ == "__main__":
    headers = {'Content-Type': 'application/json; charset=utf-8',
    "User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/74.0.3729.169 Chrome/74.0.3729.169 Safari/537.36"}
    print("dc에서 파싱할 게시글 URL을 입력해주세요")


    r = requests.get("https://gall.dcinside.com/mgallery/board/lists/?id=fromis&sort_type=N&search_head=20&page=1", headers = headers)
    bsObject = BeautifulSoup(r.text, "html.parser")

    links = []
    links2 = []
# link crawlling
    for link in bsObject.find_all('td',{'class':'gall_tit ub-word'}):
        for link2 in link.find_all('a'):
            links.append(link2.get('href'))
# filter http
    for link in links:
        if 'http' in link:
            links2.append(link)
            print(link)
    cnt = 0
    for link in links2:
        if cnt <= 3:
            cnt+=1
            continue
        name_list = []
        ri = requests.get(link, headers = headers)
        soup = BeautifulSoup(ri.text, 'html.parser')
        name(soup, name_list)
        img_link(soup, name_list, link)