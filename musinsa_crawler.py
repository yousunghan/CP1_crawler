from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import numpy as np

from urllib.request import urlopen
from urllib.parse import quote_plus

import shutil

import os, time

import urllib.request

from bs4 import BeautifulSoup
import csv

from selenium.common.exceptions import NoSuchElementException


from webdriver_manager.chrome import ChromeDriverManager

import pandas as pd

# def PageUrl(itemName, pageNum):
#     url = "https://search.musinsa.com/search/musinsa/goods?q=" + itemName + "&list_kind=small&sortCode=pop&sub_sort=&page="+ str(pageNum) +"&display_cnt=0&saleGoods=false&includeSoldOut=false&popular=false&category1DepthCode=&category2DepthCodes=&category3DepthCodes=&selectedFilters=&category1DepthName=&category2DepthName=&brandIds=&price=&colorCodes=&contentType=&styleTypes=&includeKeywords=&excludeKeywords=&originalYn=N&tags=&saleCampaign=false&serviceType=&eventType=&type=&season=&measure=&openFilterLayout=N&selectedOrderMeasure=&d_cat_cd="
#     return url

def PageUrl(categoryNum, pageNum):
    url = "https://www.musinsa.com/category/" + categoryNum + "?d_cat_cd=" + categoryNum + "&brand=&rate=&page_kind=search&list_kind=small&sort=pop&sub_sort=&page=" + str(pageNum) + "&display_cnt=90&sale_goods=&group_sale=&kids=N&ex_soldout=&color=&price1=&price2=&exclusive_yn=&shoeSizeOption=&tags=&campaign_id=&timesale_yn=&q=&includeKeywords=&measure="
    return url

def male_or_female(x):
    if x[0] == '남':
        return 0
    elif x[0] == '여':
        return 1


musinsa_data = ['bot_cot', 'bot_denim', 'bot_etc', 'bot_half', 'bot_leggins', 'bot_slax', 'bot_training', 'outer_cardigan', 'outer_fleece', 'outer_hood', 'skirt_long', 'skirt_midi', 'skirt_mini', 'top_etc', 'top_half', 'top_hood', 'top_knit', 'top_long', 'top_mantoman', 'top_pk', 'top_shirts', 'top_sleeveless']

category_num = ['003007', '003002','003006','003009','003005','003008','003004','002020','002023','002022','022003','022002','022001','001008','001001','001004','001006','001010','001005','001003','001002','001011']

musinsa_links = [
    'https://www.musinsa.com/category/003007',
    'https://www.musinsa.com/category/003002',
    'https://www.musinsa.com/category/003006',
    'https://www.musinsa.com/category/003009',
    'https://www.musinsa.com/category/003005',
    'https://www.musinsa.com/category/003008',
    'https://www.musinsa.com/category/003004',
    'https://www.musinsa.com/category/002020',
    'https://www.musinsa.com/category/002023',
    'https://www.musinsa.com/category/002022',
    'https://www.musinsa.com/category/022003',
    'https://www.musinsa.com/category/022002',
    'https://www.musinsa.com/category/022001',
    'https://www.musinsa.com/category/001008',
    'https://www.musinsa.com/category/001001',
    'https://www.musinsa.com/category/001004',
    'https://www.musinsa.com/category/001006',
    'https://www.musinsa.com/category/001010',
    'https://www.musinsa.com/category/001005',
    'https://www.musinsa.com/category/001003',
    'https://www.musinsa.com/category/001002',
    'https://www.musinsa.com/category/001011'
    ]


driver = webdriver.Chrome(ChromeDriverManager().install())

num = 0

for link in musinsa_links:
    FindingItemName = musinsa_data[num]
    category_number = category_num[num]


    pageUrl = link
    driver.get(pageUrl)

    totalPageNum = driver.find_element(By.CSS_SELECTOR, ".totalPagingNum").text

    csvfile = []
    count = 1
    
    for i in range(int(totalPageNum)):
        #페이지 수 범위
        if(i < 3) :
            pageUrl = PageUrl(category_number, i+1)
            driver.get(pageUrl)

            time.sleep(2)
     
            item_images = driver.find_elements(By.CSS_SELECTOR,".lazyload.lazy")

            #각 페이지 당 크롤링 할 제품의 수
            for i in range(len(item_images)):
                item_images[i].click()
                time.sleep(3)
                href = driver.find_element(By.CSS_SELECTOR, '.plus_cursor').get_attribute('src')
                product_name = driver.find_element(By.CSS_SELECTOR, 'span.product_title').text
                product_star = driver.find_element(By.CSS_SELECTOR, '.prd-score__rating').text
                product_sales = driver.find_element(By.CSS_SELECTOR, 'strong#sales_1y_qty').text
                product_like = driver.find_element(By.CSS_SELECTOR, 'span.prd_like_cnt').text
                product_price = driver.find_element(By.CSS_SELECTOR, 'span#list_price').text
                customer_gender = driver.find_element(By.CSS_SELECTOR, 'span.txt_gender').text
                #customer height 과 weight 은 같은 element에서 추출, 전처리 과정에서 구분할 예정 (ex: 남자 175cm 65kg)
                customer_height = driver.find_element(By.CSS_SELECTOR, 'p.review-profile__body_information').text
                customer_weight = driver.find_element(By.CSS_SELECTOR, 'p.review-profile__body_information').text
                #fit 전처리 과정에서 추출 예정
                fit = '0'
                size =  driver.find_element(By.CSS_SELECTOR, 'span.review-goods-information__option').text
                #그래프에서 크롤링하는 경우 에러가 많이 떠서 exception
                #로딩 시간을 늘리면 해결 가능할것같지만 크롤링 속도가 너무 느려져서 지금과 같은 방법을 채용
                popular_age = driver.find_element(By.CSS_SELECTOR, 'em.font-mss.graph_age').text
                #popular_gender = driver.find_element(By.CSS_SELECTOR, 'span.man.graph_sex_text').text
                popular_gender = customer_gender


                temp = []

                #csv 파일로 
                temp.append(href)
                temp.append(product_name)
                temp.append(product_star)
                temp.append(product_sales)
                temp.append(product_like)
                temp.append(product_price)
                temp.append(customer_gender)
                temp.append(customer_height)
                temp.append(customer_weight)
                temp.append(fit)
                temp.append(size)
                temp.append(popular_age)
                temp.append(popular_gender)

                csvfile.append(temp)

                
                driver.back()

                time.sleep(3)

                #iterate 할때마다 초기화 시켜줘야한다.
                item_images = driver.find_elements(By.CSS_SELECTOR,".lazyload.lazy")   

            #csvfile download
            f = open(f'{FindingItemName}.csv', 'w', encoding='utf-8', newline = '')
            csvWriter = csv.writer(f)

            for i in csvfile:
                csvWriter.writerow(i)
            

            f.close()

            # #데이터 전처리 자동화
            df = pd.read_csv(f'{FindingItemName}.csv')

            df = pd.DataFrame(np.vstack([df.columns, df]))

            df.columns = ['href', 'product_name', 'product_star', 'product_sales', 'product_like', 'product_price', 'customer_gender', 'customer_height', 'customer_weight', 'fit', 'size', 'popular_age', 'popluar_gender']


            #오류가 발생하기에 전처리과정은 잠시 생략 하였습니다, 
            #하지만 이상적으로는 data 폴더에 저장될때는 전처리과정이 끝난 상태로 저장할 예정입니다.
            # df['customer_gender'] = df['customer_gender'].apply(male_or_female)
            # df['popluar_gender'] = df['popluar_gender'].apply(male_or_female)
            # df['product_like'] = df.product_like.str.replace(',', '').astype('int64')
            # df['product_price'] = df['product_price'].str[:6]
            # # df['product_price'] = df.product_price.str.replace(',', '').astype('int64')
            # # df['customer_height'] = df['customer_height'].str[4:7]
            # # df['customer_weight'] = df['customer_weight'].str[11:13]
            # df['product_sales'] = df.product_sales.replace({'천 개 이상': "*1e3", '만 개 이상': "*1e4"}, regex = True).map(pd.eval).astype(int)
            # # #전처리된 csv 덮어씌우기
            df.to_csv(path_or_buf= f'{FindingItemName}.csv', index= False)
            
            #전처리된 df, data 폴더로 옮기기
            shutil.move(f'{FindingItemName}.csv', './data/'f'{FindingItemName}.csv')

            #df.columns = ['href', 'product_name', 'product_like', 'product_price']
            # for image in item_images:
            #     image.click()
            #     time.sleep(2)
            #     product_star = driver.find_element(By.CSS_SELECTOR, ".prd-score__link").get_attribute(".prd-score__rating")
            #     print(product_star)
    num = num + 1
            
      

driver.close()