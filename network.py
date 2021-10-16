import urllib.request
import requests
from selenium import webdriver
from bs4 import BeautifulSoup
from urllib import parse
import ssl

def delete_iframe(url):
    headers = {
        "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
    }
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    souptmp = BeautifulSoup(res.text, "html.parser")
    src_url = "https://blog.naver.com/" + souptmp.iframe["src"]
    return src_url

def text_scraping(url):
    headers = {
        "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
    }
    res = requests.get(url, headers=headers)
    res.raise_for_status()  # 문제시 프로그램 종료
    soup = BeautifulSoup(res.text, "html.parser")

    if soup.find("div", attrs={"class": "se-main-container"}):
        text = soup.find("div", attrs={
            "class": "se-main-container"
        }).get_text()
        text = text.replace("\n", "")  # 공백 제거
        return text
    else:
        return "확인불가"


def cafe_crawler2(url, name):
    driver = webdriver.PhantomJS(
        "C:\\Users\\김훈기\\OneDrive - konkuk.ac.kr\\바탕 화면\\phantomjs-2.1.1-windows\\bin\\phantomjs"
    )
    driver.get(url)
    driver.switch_to_frame('cafe_main')
    page_source = driver.page_source
    if page_source.count(name) > 0:
        return True
    else:
        return False

def counting(name, key):
    context = ssl._create_unverified_context()
    search = key
    url = (
        "https://search.naver.com/search.naver?where=view&sm=tab_jum&query=" +
        parse.quote(search))
    html = urllib.request.urlopen(url, context=context).read()
    soup = BeautifulSoup(html, "html.parser")
    title = soup.find_all(class_="api_txt_lines total_tit _cross_trigger")
    cnt = 0
    flag = False
    for i in title:
        if flag == True:
            break
        cnt += 1
        if cnt == 7:
            break
        print(i.attrs["href"])
        urltmp = i.attrs["href"]
        if urltmp.find("blog") > 0:
            print('blog')
            durl = delete_iframe(urltmp)
            contents = text_scraping(durl)
            if contents.find(name) > 0:
                flag = True
                print(contents.find(name))
        elif urltmp.find("cafe") > 0:
            flag = cafe_crawler2(urltmp, name)
    if flag == True:
        return cnt
    else:
        return -1
