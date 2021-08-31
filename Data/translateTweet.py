import getpass
import calendar
import time
import re as reg
import platform
import sys
import requests
import urllib.request


from bs4 import BeautifulSoup, NavigableString, Tag

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains


# -------------------------------------------------------------
# -------------------------------------------------------------


# Global Variables

driver = None

def goToTranslate():
    """ Logging into our own profile """

    try:
        global driver

        options = Options()

        #  Code to disable notifications pop up of Chrome Browser
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-infobars")
        options.add_argument("--mute-audio")
        # options.add_argument("headless")

        try:
            platform_ = platform.system().lower()
            if platform_ in ['linux', 'darwin']:
                driver = webdriver.Chrome(executable_path="./chromedriver", options=options)
            else:
                driver = webdriver.Chrome(executable_path="./chromedriver.exe", options=options)
        except:
            print("Kindly replace the Chrome Web Driver with the latest one from"
                  "http://chromedriver.chromium.org/downloads"
                  "\nYour OS: {}".format(platform_)
                 )
            exit()

        driver.get("https://translate.google.com") # go to facebook home page
        driver.maximize_window()

        time.sleep(30)

        try:

            f=open('C:\\Users\\Alvi Rahman\\Desktop\\Farhana Miss\\Data\\banglaTweets.txt',mode="r", encoding="utf-8")
            tweets=f.readlines()
            f.close()

            tweets=[s.replace('\n','') for s in tweets]

            output_file=open("translated_tweet.txt", mode="w", encoding="utf-16")

            inputBox=driver.find_element_by_id('source')

            tweet_count = 0
            for i in range (8001,12000):
                inputBox.send_keys(tweets[i])
                translatedTweet = "xxxxxxxxxxxx"
                time.sleep(10)

                try:

	                TranslationBox=driver.find_element_by_xpath("/html/body/div[2]/div[1]/div[2]/div[1]/div[1]/div[2]/div[3]/div[1]/div[2]/div/span[1]/span")
	                translatedTweet = TranslationBox.text

	                translatedTweet=translatedTweet.replace('\b',' ')
	                translatedTweet=translatedTweet.replace('\n',' ')
	                translatedTweet=translatedTweet.replace('\t',' ')
	                translatedTweet=translatedTweet.replace('\r',' ')
	                translatedTweet=translatedTweet.replace('\f',' ')
	                translatedTweet=reg.sub(' +',' ',translatedTweet)

                except:
                    pass


            output_file.writelines(translatedTweet+"\n")
            inputBox.clear()
            tweet_count = tweet_count + 1

            if tweet_count%100 ==0:
                time.sleep(270)

            elif tweet_count%50 ==0:
                time.sleep(150)

            elif tweet_count%10 ==0:
                time.sleep(60)

            output_file.close()
            driver.close()

        except:
            exc_type = sys.exc_info()[0]
            exc_tb = sys.exc_info()[2]
            print(exc_type, exc_tb.tb_lineno)
            pass

        # filling the form
        # driver.find_element_by_name('email').send_keys(email)
        # driver.find_element_by_name('pass').send_keys(password)

        # # clicking on login button
        # driver.find_element_by_id('loginbutton').click()

        print("Successfully logged in")

    except Exception as e:
        print("There's some error in log in.")
        print(sys.exc_info()[0])
        exit()


# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
def main():

    goToTranslate()
# -------------------------------------------------------------
# -------------------------------------------------------------
# -------------------------------------------------------------

if __name__ == '__main__':
    # get things rolling
    main()
