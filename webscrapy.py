from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from bs4 import BeautifulSoup
# options = ChromeOptions()
# options.add_argument("--start-maximized")
# driver = ChromeDriver(options)
import time
import os
import ast
import urllib.request

# define the name of the directory to be created
# path = os.getcwd()
# path = "/tmp/year"

# try:
#     os.mkdir(path)

def get_string(str):
    alphanumeric = ""
    for character in str:
        if character.isalnum():
            alphanumeric += character
        else:
            alphanumeric += '_'
    return alphanumeric
PINNUM = '0962'
CARDNUM = '2536871'
driver = webdriver.Chrome(ChromeDriverManager().install())
# driver.maximize_window()
url = "http://lynda.com/portal/sip?org=houstonlibrary.org"
driver.get(url) 
cardnumber = driver.find_element_by_id('card-number')
cardpin = driver.find_element_by_id('card-pin')
loginbut = driver.find_element_by_id('submit-library-card')
cardnumber.send_keys(CARDNUM)
cardpin.send_keys(PINNUM)
loginbut.click()
url1 = 'https://www.lynda.com/PowerPoint-tutorials/PowerPoint-Tips-Weekly/534644-2.html'
driver.get(url1) 

# Left_header = driver.find_elements_by_xpath('//*[contains(@class, "course-toc") and contains(@class, "course-toc") and contains(@class, "autoscroll")]')

soup = BeautifulSoup(driver.page_source, 'html.parser')

Left_header = soup.find("ul", {"class": "course-toc toc-container autoscroll"})
video = soup.find('video', {'class': 'player'})
title = soup.find('h1', {'class': 'default-title'}).text
# print(type(video.get('data-conviva')))
print(ast.literal_eval(video.get('data-conviva'))['Url']) 
# print(video.get('data-conviva').get('Url'))

Lilist = Left_header.find_all('li', {'role': 'presentation'}, recursive=False)
# print(Lilist)
urldic = {}
# print('Lilist', len(Lilist))

for Li in Lilist:
    key = Li.find('h4').text
    lidic = {}
    Lilis = Li.find_all('li', {'class': 'toc-video-item'})
    print('Lilis', len(Lilis))
    for lili in Lilis:
        ky = lili.find('span', {'class': 'sr-only'}).text
        lidic[ky] = lili.find('a')['href']
        # print(lili.find('a'))
    urldic[key] = lidic
print(urldic)


path = os.getcwd()
pathpart = path.split('\\')
path = '/'.join(pathpart)
path = path +'/'+ get_string(title)  
try:   
    os.mkdir(path)
except:
    pass


for key, val in urldic.items():
    print(type(val))
    path0 = path + '/' + get_string(key)
    try:   
        os.mkdir(path0)
    except:
        pass
    for ky, vl in val.items():
        path1 = path0+ '/' + get_string(ky)
        try:   
            os.mkdir(path1)
        except:
            pass
        driver.get(vl)
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        video = soup.find('video', {'class': 'player'})

        # print(type(video.get('data-conviva')))
        videourl = ast.literal_eval(video.get('data-conviva'))['Url'] 
        filename = path1 + '/' + get_string(ky) + '.mp4'
        f= open(filename,"w+")
        def waitsuccess(kk):
            try:
                urllib.request.urlretrieve(videourl, filename) 
                return
            except:
                time.sleep(kk)
                return waitsuccess(kk * 2)
        waitsuccess(1)
        f.close()
        transcript = soup.find("section", {"id": "tab-transcript"}).find('div', {'class': 'row transcripts video-transcripts'}).text
        file = open(path1 + '/transcript.txt', 'w+')
        file.write(transcript)
        file.close()
        print(transcript)
        overview = soup.find("section", {"id": "tab-overview"}).find('div', {'itemprop': 'description'}).text
        file = open(path1 + '/overview.txt', 'w+')
        file.write(overview)
        file.close()
        print(overview)
