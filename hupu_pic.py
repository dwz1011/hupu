import urllib.request as ul
import urllib
import json
import os
import re
import time
import sys
import shutil
import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup as bs



driver = webdriver.PhantomJS(executable_path=r"/Users/edz/Downloads/phantomjs-2.1.1-macosx/bin/phantomjs")

wait = ui.WebDriverWait(driver,10)

def loadPicture(pic_urls, pic_path):

    for pic_url in pic_urls:
        # 删除路径获取图片名字
        pic_name = os.path.basename(pic_url)
        # 去除'*' 防止错误 invalid mode ('wb') or filename
        pic_name = pic_name.replace('*', '')
        urllib.request.urlretrieve(pic_url, pic_path + pic_name)


#爬取具体的图片及下一张
def getScript(elem_url, path, nums):
    try:
        #由于链接 http://photo.hupu.com/nba/p29556-1.html
        #只需拼接 http://..../p29556-数字.html 省略了自动点击"下一张"操作
        count = 1
        t = elem_url.find(r'.html')
        while (count <= nums):
            html_url = elem_url[:t] + '-' + str(count) + '.html'
            #print html_url
            '''
            driver_pic.get(html_url)
            elem = driver_pic.find_element_by_xpath("//div[@class='pic_bg']/div/img")
            url = elem.get_attribute("src")
            '''
            content = ul.urlopen(html_url).read()

            bsobj = bs(content, 'html.parser')

            pic_s = bsobj.find('div', {'class': 'tongbox'})
            urls = []
            ps = pic_s.find_all('img')
            for link in ps:
                url = 'http:'+link['oksrc'].replace('_60x60', '')
                urls.append(url)

            loadPicture(urls, path)

            count = count + 1
    except Exception as e:
        print('Error:',e)
    finally:
        print('Download ' + str(count) + ' pictures\n')


def getTitle(url):
    try:
        # 爬取url和标题
        count = 0
        print('Function getTitle(key,url)')
        driver.get(url)
        wait.until(lambda driver: driver.find_element_by_xpath("//div[@class='piclist3']"))
        print('Title: ' + driver.title + '\n')
        # 缩略图片url(此处无用) 图片数量 标题(文件名) 注意顺序
        elem_url = driver.find_elements_by_xpath("//a[@class='ku']/img")
        elem_num = driver.find_elements_by_xpath("//div[@class='piclist3']/table/tbody/tr/td/dl/dd[1]")
        elem_title = driver.find_elements_by_xpath("//div[@class='piclist3']/table/tbody/tr/td/dl/dt/a")

        for url in elem_url:
            pic_url = url.get_attribute("src")
            html_url = elem_title[count].get_attribute("href")
            print(elem_title[count].text)
            print(html_url)
            print(pic_url)
            print(elem_num[count].text)
            # 创建图片文件夹
            path = elem_title[count].text+'/'
            if os.path.isfile(path):
                os.remove(path)
            elif os.path.isdir(path):
                shutil.rmtree(path, True)

            os.makedirs('hupu/images/'+path)

            m = re.findall(r'\d{1,}', elem_num[count].text)
            nums = int(m[0])
            count += 1

            getScript(html_url, 'hupu/images/'+path, nums)

    except Exception as e:
        print('Error:', e)

    finally:
        print('Find ' + str(count) + ' pages with key\n')





def main():

    # Create Folder
    if not os.path.exists('images'):
        os.mkdir('images')

    # key = input("Please input a key: ").decode(sys.stdin.encoding)
    # print('The key is : ' + key)
    print('Ready to start the Download!!!\n\n')
    starttime = datetime.datetime.now()

    num = 1

    while num <= 1:
        url = 'http://photo.hupu.com/nba/tag/%E9%A9%AC%E5%88%BA'
        print('第' + str(num) + '页', 'url:' + url)
        getTitle(url)
        time.sleep(2)
        num += 1
    else:
        print('Download Over!')

    endtime = datetime.datetime.now()

    print('The Running time : ', (endtime - starttime).seconds)

main()






