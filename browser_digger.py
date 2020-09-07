from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.common.by import By

import urllib
from urllib.request import urlretrieve
import time
import pandas as pd


class Digger:

    def __init__(self):
        self.digger = webdriver.Chrome(ChromeDriverManager().install())
        self.url = 'https://finance.yahoo.com/'
        self.digger.get(self.url)
        self.wait = WebDriverWait(self.digger, 3000)

    def url_(self):
        self.digger.get(self.url)

    def find_company(self, name_company):
        submit_key = self.wait.until(EC.presence_of_element_located(
            (
                By.ID,
                'header-desktop-search-button'
            )))
        my_search = self.wait.until(EC.presence_of_element_located(
            (
                By.ID,
                'yfin-usr-qry'
            )))
        time.sleep(5)
        my_search.send_keys(name_company)
        time.sleep(5)
        submit_key.send_keys(Keys.ENTER)
        return True if self.url in self.digger.current_url else False

    def download_his_data(self, name_company):
        time.sleep(5)
        # click to historical data
        self.digger.find_element_by_link_text('Historical Data').click()
        time.sleep(5)
        # time_period
        self.digger.find_element_by_xpath(
            "//section/div[1]/div[1]/div[1]/div/div/div/span").click()
        time.sleep(5)
        # max_period company work
        self.digger.find_element_by_xpath(
            "//div/ul[2]/li[4]/button/span").click()
        # get link for download historical data
        link_for_download = self.digger.find_element_by_xpath(
            "//section/div[1]/div[2]/span[2]/a").get_attribute('href')
        # download historical data
        urllib.request.urlretrieve(
            link_for_download, filename=name_company + ".csv")

    def news_last_to_file(self, name_company):
        # click to news
        self.digger.find_element_by_link_text("Summary").click()
        time.sleep(5)
        try:
            time.sleep(5)
            news_link = self.digger.find_element_by_xpath(
                "//ul/li[1]/div/div[1]/div[2]/h3/a").get_attribute('href')
            news_titel = self.digger.find_element_by_xpath(
                "//ul/li[1]/div/div[1]/div[2]/h3/a").text
        except NoSuchElementException:
            # the item can be without a picture
            time.sleep(5)
            news_link = self.digger.find_element_by_xpath(
                "//ul/li[1]/div/div/div[1]/h3/a").get_attribute('href')
            news_titel = self.digger.find_element_by_xpath(
                "//ul/li[1]/div/div/div[1]/h3/a").text
        # create file for news vs titel
        with open(name_company + "_news.csv", "w") as news:
            news.write("link :" + news_link + "\n")
            news.write("title :" + news_titel)

    def add_new_column(self, name_company):
        """
        
        """
        csv_input = pd.read_csv(name_company + '.csv')
        # create column and input date
        csv_input['3day_before_change'] = csv_input['Close']
        # change list ratio of data today to 3 days
        close_list = csv_input['3day_before_change'].tolist()
        for count in range(len(close_list)):
            if len(close_list) - count < 4:
                close_list[count] = 0
            else:
                close_list[count] = float(close_list[count]) / float(
                    close_list[count + 3])
        # add column to table vs value
        csv_input['3day_before_change'] = close_list
        # save changes
        csv_input.to_csv(name_company + '.csv')
