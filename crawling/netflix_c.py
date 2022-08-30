# 넷플릭스 크롤링을 위한 코드
# please lock this source code
# that code will be tirgered security exploit

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import csv

# 브라우저 열기
browser = webdriver.Chrome()
url = "https://www.netflix.com/kr/"
browser.get(url)
browser.maximize_window()

# time.sleep(3)
login = browser.find_element_by_class_name("authLinks")
login.click()

# login 과정 진행
id = browser.find_element_by_name("userLoginId").send_keys("***************")  # 개인 아이디 패스워드 입력하기
pw = browser.find_element_by_name("password").send_keys("*****************")
browser.find_element_by_class_name("btn-submit").click()
time.sleep(3)
browser.find_element_by_xpath('//*[@id="appMountPoint"]/div/div/div[1]/div[1]/div[2]/div/div/ul/li[3]/div/a/div/div').click()
# time.sleep(5)
browser.find_element_by_xpath('//*[@id="appMountPoint"]/div/div/div[1]/div[1]/div[2]/div/div[3]/div/input[1]').send_keys("2")
browser.find_element_by_xpath('//*[@id="appMountPoint"]/div/div/div[1]/div[1]/div[2]/div/div[3]/div/input[2]').send_keys("0")
browser.find_element_by_xpath('//*[@id="appMountPoint"]/div/div/div[1]/div[1]/div[2]/div/div[3]/div/input[3]').send_keys("0")
browser.find_element_by_xpath('//*[@id="appMountPoint"]/div/div/div[1]/div[1]/div[2]/div/div[3]/div/input[4]').send_keys("2")


# move to source
time.sleep(5)
browser.find_element_by_xpath('//*[@id="appMountPoint"]/div/div/div[1]/div[1]/div[1]/div/div/ul/li[4]/a').click()
time.sleep(5)
browser.find_element_by_xpath('//*[@id="appMountPoint"]/div/div/div[1]/div[1]/div[1]/div/div[2]/div/div/div/div[2]/div[2]/div/button').click()
time.sleep(5)

# 크롤링 진행하기
# 일단 페이지를 모두 로드한다.
interval = 2
prev_height = browser.execute_script("return document.body.scrollHeight")

# 높이 변화가 없을 때 까지 스크롤을 내린다.
while True:
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    time.sleep(interval)
    curr_height = browser.execute_script("return document.body.scrollHeight")

    if prev_height == curr_height:
        break

    prev_height = curr_height
print('scroll end')

# 클릭을 해서 정보를 가져오기 전에 일단 모든 이미지를 긁어온다.
# 어차피 url은 사용도 못하므로 정보자체를 저장하지 않는다.

curr_html = browser.page_source
soup = BeautifulSoup(curr_html, "html.parser")
dummys = soup.find_all("a", attrs={"class":"slider-refocus"})
name_ls = []
for idx, dummy in enumerate(dummys):
    name = dummy.get_text()
    name_ls.append(name)
    # image_url = dummy.img["src"]
    # print(image_url)

    # image_res = requests.get(image_url)
    # image_res.raise_for_status()

    # try:
    #     with open("{0}.jpg".format(name), 'wb') as f:
    #         f.write(image_res.content)
    #         # time.sleep(0.3)
    # except:
    #     pass

# csvfile gen
f = open("netflix_movie.csv", "w", encoding="utf-8-sig", newline="")
writer = csv.writer(f)
title = ["index", "name", "synopsis", "genre", "netflix", "tiving"]
writer.writerow(title)

# 한개 씩 클릭가능한 코드 만들기
elems = browser.find_elements_by_class_name('slider-item')
for i, elem in enumerate(elems):
    if i <= 624:
        pass
    else:
        try:
            data = []
            data.append(i)
            data.append(name_ls[i])
            elem.click()
            time.sleep(2)

            html = browser.page_source
            soup = BeautifulSoup(html, 'html.parser')
            synopsis = soup.find("p", attrs={"class":"preview-modal-synopsis"}).get_text()
            genre = soup.find("div", attrs={"data-uia":"previewModal--tags-genre"}).get_text().replace('장르: ', '')

            data.append(synopsis)
            data.append(genre)
            # netflix 는 2번째 인덱스를 1
            data.append(1)
            # Tving 은 3번째 인덱스를 1
            data.append(0)
            writer.writerow(data)
            print(data) # csv file로 저장하기 전 테스트 출력
            browser.find_element_by_class_name("previewModal-close").click()
            time.sleep(2)
        except:
            print("pass")
            try:
                browser.find_element_by_class_name("previewModal-close").click()
            except:
                pass