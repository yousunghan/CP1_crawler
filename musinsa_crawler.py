from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from urllib.request import urlopen
from urllib.parse import quote_plus

import os, time

import urllib.request

from bs4 import BeautifulSoup
import csv

import schedule

#search by item name
def PageUrl(itemName, pageNum):
    url = "https://search.musinsa.com/search/musinsa/goods?q=" + itemName + "&list_kind=small&sortCode=pop&sub_sort=&page="+ str(pageNum) +"&display_cnt=0&saleGoods=false&includeSoldOut=false&popular=false&category1DepthCode=&category2DepthCodes=&category3DepthCodes=&selectedFilters=&category1DepthName=&category2DepthName=&brandIds=&price=&colorCodes=&contentType=&styleTypes=&includeKeywords=&excludeKeywords=&originalYn=N&tags=&saleCampaign=false&serviceType=&eventType=&type=&season=&measure=&openFilterLayout=N&selectedOrderMeasure=&d_cat_cd="
    return url

FindingItemName = input("추천받은 product_name : ")
#"980g pigment mtm"

driver = webdriver.Chrome(os.getcwd() + "/chromedriver")

pageUrl = PageUrl(FindingItemName, 1)
driver.get(pageUrl)

totalPageNum = driver.find_element(By.CSS_SELECTOR, ".totalPagingNum").text
#print("Total Page of ", FindingItemName, " : ", str(totalPageNum))

csvfile = []

count = 1
for i in range(int(totalPageNum)):
    if(i < 3) :
        pageUrl = PageUrl(FindingItemName, i+1)
        driver.get(pageUrl)

        time.sleep(2)

        item_infos = driver.find_elements(By.CSS_SELECTOR,".img-block")
        item_images = driver.find_elements(By.CSS_SELECTOR,".lazyload.lazy")
        #span class 에 있는 price
        item_span = driver.find_elements(By.CSS_SELECTOR, "span.count")

        print("Finding: ", FindingItemName, " - Page ", i+1, "/",totalPageNum, " start - ", len(item_infos), " items exist")
        #img download
        for i in range(len(item_infos)):
            try:
                time.sleep(0.5)

                product_name = item_infos[i].get_attribute("title")
                imgUrl = item_images[i].get_attribute("data-original")
                product_price = item_infos[i].get_attribute("data-bh-content-meta3")
                product_like = item_span[i].text

                temp = []
                
                temp.append(imgUrl)
                temp.append(product_name)
                temp.append(product_like)
                temp.append(product_price)
                csvfile.append(temp)

                # Save Image ****
                #urllib.request.urlretrieve(img_url, "./img" + str(i+1) + ".jpg")

            except Exception as e:
                print(e)
                pass

            
        #csvfile download
        f = open(f'{FindingItemName}.csv', 'w', encoding='utf-8', newline = '')
        csvWriter = csv.writer(f)

        for i in csvfile:
            csvWriter.writerow(i)
        
        f.close()


        # for image in item_images:
        #     image.click()
        #     time.sleep(2)
        #     product_star = driver.find_element(By.CSS_SELECTOR, ".prd-score__link").get_attribute(".prd-score__rating")
        #     print(product_star)



        

driver.close()