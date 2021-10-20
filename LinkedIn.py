# Download geckodriver drive from https://github.com/mozilla/geckodriver/releases

import os
import re
import time
import random
import pandas as pd

from bs4 import BeautifulSoup
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Firefox(executable_path=os.path.join(os.getcwd(), "geckodriver.exe"))

word_checker = ['hiring','hire','opening','jobs', 'jobsearch', 'recruitment','job','nowhiring','jobopening', 'jobhunt', 'jobseeker', 'applynow', 'recruiter', 'jobopportunity', 'jobinterview', 'jobsearching','opportunity']

df = pd.DataFrame(columns = ['name','text','link','time'])
df.to_csv('posts.csv',index=False)

df = pd.read_csv('posts.csv')
df.head()
 
def startup(tag):
    # create url for hasttags 
    df = pd.read_csv('posts.csv')
    #df = pd.DataFrame(columns = ['name','text','link'])
    url = 'https://www.linkedin.com/feed/hashtag/' + tag
    
    #get urls
    hashtag = driver.get(url)
    input("Please Enter once you login to your LinkedIn A/C. [Return] ")

    #sort posts by recents from top
    filters = driver.find_element_by_xpath("//button[contains(string(),'Sort by:')]").click()
    filters = driver.find_element_by_xpath("//div[@class = 'artdeco-dropdown__content-inner']//button[contains(string(),'Recent')]").click()
    
    #scroll posts for 200 pages
    body = driver.find_element_by_css_selector('body')
    for i in range(10):
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(random.randint(1, 4))
    
    #click see more for all texts
    see_more=driver.find_elements_by_xpath("//button[@class = 'feed-shared-inline-show-more-text__see-more-less-toggle see-more t-14 t-black--light t-normal hoverable-link-text']")
    for i in see_more:
        i.click()
    
    # get all posts
    time.sleep(10)
    posts = driver.find_elements_by_xpath("//div[@class = 'relative' and contains(@data-id,'urn:li:activity')]")
    
    # loop on each post, get name, url, text of the post and append into the dataframe
    for i in posts:
        try:
            data = {}
            soup = BeautifulSoup(i.get_attribute('innerHTML'))
        
            names = soup.find('a',attrs = {'data-control-name':'actor_container'},href=True)
            data['name'] = names.find('span',attrs = {'dir':'ltr'}).text
            data['link'] = names.attrs['href']
            texts = soup.find('div',attrs = {'class':'feed-shared-update-v2__description-wrapper'}).text
            texts = re.sub("[^0-9a-zA-Z ]"," ",texts)
            data['text'] = texts.strip()
            now = datetime.now()
            current_time = now.strftime("%D:%H:%M:%S")
            data['time'] = current_time 
            for req in word_checker:
                if req in data['text']:
                    df = df.append(data, ignore_index=True)
                    break
                else:
                    pass
        except Exception as E:
            pass
    df = df.drop_duplicates(subset ="text")
    time.sleep(random.randint(1, 4))
    df.to_csv('posts.csv',index=False)
    

startup('devops')