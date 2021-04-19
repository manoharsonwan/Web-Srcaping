
from selenium import webdriver
from selenium.webdriver.common.keys import Keys                                            
import time
import pandas as pd
from openpyxl import Workbook


# # from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC



import selenium
from selenium import webdriver as wb

def web_scraping(fromdate, todate, keyword):

    # Chrome Diriver install in local machine, need to change while running in another machine 
    driver=wb.Chrome('/home/manohar/Desktop/chromedriver_linux64/chromedriver')
    driver.get('https://www.eurex.com/ex-en/find/circulars/')


    ######### Step 1 ################
    # Loading the correct date range
    # input value from_date 
    search = driver.find_element_by_name("dateFrom")
    #sending form date valu
    search.send_keys(fromdate)
    # input value from_date
    search = driver.find_element_by_name("dateTo")
    #sending form date valu
    search.send_keys(todate)
    #wait the browser for 30 sesconds untill page complitelly open
    time.sleep(30)
    # after entering the range date click on search butten
    driver.find_element_by_xpath('//*[@id="search-form"]/div/div[2]/div/div[2]/div/button[2]').click()

    ########### Step 2 #######
    # Filtering of circulars
    list_of_result = []
    # keyword = 'stock'
    condition=True
    while condition:
        productInfoList=driver.find_elements_by_class_name('dbx-search-result')
        for el in productInfoList:
            search_title = el.find_element_by_tag_name('h3')
            search_title_text =search_title.text.lower().split()

            if keyword in  search_title_text:
                title = ' '.join(search_title_text)
                print('title:', title)
                search_date = el.find_element_by_class_name('dbx-search-result__date')
                search_date = search_date.text
                print('search_date:', search_date)
                search_tag = el.find_element_by_class_name('dbx-search-result__tagline')
                search_tag = search_tag.text
                print('search_tag:', search_tag)

                search_title = el.find_element_by_tag_name('a')
    #             search_title_text = search_title.text
                hyper_link = search_title.get_property('href')
                print('hyper_link:', hyper_link)

                dict_templete = {'circular title':title,
                                'Release date':search_date,
                                'Tags':search_tag,
                                'URL':hyper_link}
                list_of_result.append(dict_templete)
        try:
            driver.find_element_by_xpath('//*[@id="search-form"]/nav/ul/li[9]/button').click()
         
        except:
            condition=False
    ########### Step 3 Saving Results into CSV
 
    pd.DataFrame(list_of_result)
    df = pd.DataFrame(list_of_result)
    df.to_csv('finstinct.csv')
    df.to_excel('finstinct_xlsx.xlsx')
    

web_scraping("12/1/2020", "12/3/2021", "stock")