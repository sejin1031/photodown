from bs4 import BeautifulSoup
import re
import requests
import urllib
from urllib.request import urlopen
import sys

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
        urllib.request.urlretrieve(string_img_url, "./dcinside/." + name_list[i])

def name(soup, name_list):
    try: 
        ul_class = soup.find("ul", class_="appending_file")
        a_tags = ul_class.find_all("a")
        for i in range(0, len(a_tags), 1):
            string_name = str(a_tags[i])
            tmp_start_namePoint = string_name.find(">")
            tmp_end_namePoint = string_name.find("</a>")
            string_name = string_name[tmp_start_namePoint + 1 : tmp_end_namePoint]
            name_list.append(string_name)
            print(string_name)
        name_list.sort()
    except AttributeError :
        print("error") 


def debuging_request(r):
    f = open("debuger.txt", mode="wt", encoding="utf-8")
    f.write(r)
    f.close()

if __name__ == "__main__":
    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'ko-KR,ko;q=0.9,ja-JP;q=0.8,ja;q=0.7,en-US;q=0.6,en;q=0.5',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Host': 'gall.dcinside.com',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36'
    }
    print("dc에서 파싱할 게시글 URL을 입력해주세요")


    r = requests.get("https://gall.dcinside.com/mgallery/board/lists/?id=fromis&sort_type=N&search_head=20&page="+str(sys.argv[1]), headers = headers)
    bsObject = BeautifulSoup(r.text, "html.parser")

    links = []

    for link in bsObject.find_all('td',{'class':'gall_tit ub-word'}):
        for link2 in link.find_all('a'):
            link3 = link2.get('href')
            if 'http' in link3 and int(link3[60:66]) != 559808 and int(link3[60:66]) != 510845 and int(link3[60:66]) != 431773 and int(link3[60:66]) != 431734    :
                link3 = link3[0:67] + "page=1"
                links.append(link3)

    for i in range(5,len(links)):
        name_list = []
        ri = requests.get(links[i], headers = headers)
        soup = BeautifulSoup(ri.text, 'html.parser')
        name(soup, name_list)
        img_link(soup, name_list, links[i]) 