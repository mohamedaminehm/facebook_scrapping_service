from typing import Text
from bs4 import BeautifulSoup 
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager 
from selenium.webdriver.chrome.options import Options
import time
import json
from fastapi import FastAPI
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from settings import get_db


db = get_db()


class Scraper():
    def __init__(self, page):
        self.page = page
        self.url_page = f"https://m.facebook.com/{self.page}"

        self.s=Service(ChromeDriverManager().install())

        self.chrome_options = Options()
        self.chrome_options.add_argument('--headless')
        self.chrome_options.add_argument('--no-sandbox')
        self.chrome_options.add_argument('--disable-dev-shm-usage')

    def scrolling_pages(self,driver):

        pause_time = 2
        scrolled_pages = 0
        last_scroll_height = driver.execute_script("return document.body.scrollHeight")

        while scrolled_pages < 5:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            scrolled_pages +=1
            time.sleep(pause_time)
            
            
    def scraping(self):
        driver = webdriver.Chrome(service=self.s,chrome_options=self.chrome_options)
        driver.get(self.url_page)
        scraped_data = {
            "post_text" : [],
            "reactions" : [],
            "comments" : []
        }
        self.scrolling_pages(driver)
        html = BeautifulSoup(driver.page_source,'lxml')


        with open("mapper.json") as j :
            mapper = json.load(j)

        sections = html.findAll('div',{'class':'_3drp'})

        
        for s in sections:
            for e in mapper["fields"]:
                try:
                    subsec = s.find(e["tag"], attrs = {'class':e["class"]})
                    if e["field"] == "post_text":
                        subsec = subsec.find("p").get_text(strip=True) 
                    elif e["field"] == "reactions" or e["field"] == "comments":
                        subsec = subsec.get_text(strip=True).split()[0]
                    scraped_data[e["field"]].append(subsec) if subsec != None and subsec != "" else  scraped_data[e["field"]].append('NA')
                except Exception as ex:
                    scraped_data[e["field"]].append('NA')
        return scraped_data

    async def save_records(self, scraped_data):
        for i in range(len(scraped_data["post_text"])):
            item = {
                    "text" : scraped_data["post_text"][i],
                    "reactions" : scraped_data["reactions"][i],
                    "comments" : scraped_data["comments"][i]
                }
            item = await db[self.page].insert_one(item)
        posts = await db[self.page].find().to_list(30)
        for i in range(len(posts)):
            posts[i]["_id"] = str(posts[i]["_id"])
        return posts
    
    async def get_all(self):
        posts = []
        async for p in db[self.page].find():
            p["_id"] = str(p["_id"])
            posts.append(p)
        return posts