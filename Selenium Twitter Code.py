# -*- coding: utf-8 -*-
"""
Created on Thu Nov 24 00:58:38 2022

@author: userpc
"""

import csv
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep


def get_tweet_data(card):
        
    cards = driver.find_elements(By.XPATH,"//article[@data-testid='tweet']")
    UserTag = card.find_element(By.XPATH,".//span").text

    TimeStamp = card.find_element(By.XPATH,".//time").get_attribute('datetime')

    comment = card.find_element(By.XPATH,".//div[2]/div[2]/div[1]").text
    responding = card.find_element(By.XPATH,".//div[2]/div[2]/div[2]").text

    text = comment+responding

    Reply = card.find_element(By.XPATH,".//div[@data-testid='reply']").text
            
    reTweet = card.find_element(By.XPATH,".//div[@data-testid='retweet']").text
            
    Like = card.find_element(By.XPATH,".//div[@data-testid='like']").text

    tweet = (UserTag, TimeStamp,text ,Reply, reTweet, Like)
    
    return tweet


subject = "#pfizer"

PATH = "C:\Program Files\drivers\chromedriver.exe"
driver = webdriver.Chrome(PATH)
driver.get("https://twitter.com/login")


# Setup the log in
sleep(20)
username = driver.find_element(By.XPATH,"//input[@name='text']")
username.send_keys("EmdadImu")
next_button = driver.find_element(By.XPATH,"//span[contains(text(),'Next')]")
next_button.click()

sleep(15)
password = driver.find_element(By.XPATH,"//input[@name='password']")
password.send_keys('@PASS123*@')
log_in = driver.find_element(By.XPATH,"//span[contains(text(),'Log in')]")
log_in.click()

# Search item and fetch it
sleep(15)
search_box = driver.find_element(By.XPATH,"//input[@data-testid='SearchBox_Search_Input']")
search_box.send_keys(subject)
search_box.send_keys(Keys.ENTER)

sleep(15)
tab = driver.find_element("link text", "Latest")
tab.click()

data = []
tweet_ids = set()
last_position = driver.execute_script("return window.pageYOffset;")

scrolling = True
data = []
tweet_ids = set()
last_position = driver.execute_script("return window.pageYOffset;")
scrolling = True

while scrolling:
    page_cards = driver.find_elements(By.XPATH,"//article[@data-testid='tweet']")
    for card in page_cards[-15:]:
        tweet = get_tweet_data(card)
        if tweet:
            tweet_id = ''.join(tweet)
            if tweet_id not in tweet_ids:
                tweet_ids.add(tweet_id)
                data.append(tweet)
            
    scroll_attempt = 0
    while True:
        # check scroll position
        print("4")
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        sleep(2)
        curr_position = driver.execute_script("return window.pageYOffset;")
        if last_position == curr_position:
            scroll_attempt += 1
            
            # end of scroll region
            if scroll_attempt >= 3:
                scrolling = False
                break
            else:
                sleep(2) # attempt another scroll
        else:
            last_position = curr_position
            break

# close the web driver
driver.close()
print(data)

with open('tweet.csv','w',newline='',encoding = 'utf-8') as f:
    header = ['UserTag', 'TimeStamp','text' ,'Reply', 'reTweet', 'Like']
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(data)

