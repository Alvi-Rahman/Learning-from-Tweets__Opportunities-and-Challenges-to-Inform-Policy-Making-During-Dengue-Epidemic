import getpass
import calendar
import time
import platform
import sys
import requests
import urllib.request

from bs4 import BeautifulSoup

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

total_scrolls = 20000
current_scrolls = 0
scroll_time = 5

old_height = 0

def login(email, password):
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

        driver.get("https://www.facebook.com") # go to facebook home page
        driver.maximize_window() 

        # filling the form
        driver.find_element_by_name('email').send_keys(email)
        driver.find_element_by_name('pass').send_keys(password)

        # clicking on login button
        driver.find_element_by_id('loginbutton').click()

        print("Successfully logged in")

    except Exception as e:
        print("There's some error in log in.")
        print(sys.exc_info()[0])
        exit()


# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------

def searchKeyword():

    try:
        WebDriverWait(driver,30).until(EC.presence_of_element_located((By.NAME,"q"))) #wait to find search bar
        search_bar=driver.find_element_by_name('q') #find search bar
        search_bar.send_keys("#airportroadaccident") #write query in search bar
        search_bar.send_keys(Keys.RETURN) #press enter with written query
        print("searched with the keyword successfully!")

    except Exception as e:
        print("There's some error to find search bar.")
        print(sys.exc_info()[0])
        time.sleep(60)
        search_bar.send_keys(Keys.RETURN) #press enter with written query
        print("searched with the keyword successfully!")
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------

def check_height():
    new_height = driver.execute_script("return document.body.scrollHeight")
    return new_height != old_height


# -------------------------------------------------------------
# -------------------------------------------------------------

def scroll():
    global old_height
    current_scrolls = 0

    while (True):
        try:
            if current_scrolls == total_scrolls:
                return

            old_height = driver.execute_script("return document.body.scrollHeight")
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            WebDriverWait(driver, scroll_time, 0.05).until(lambda driver: check_height())
            current_scrolls += 1
        except TimeoutException:
            break

    return

    
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
def scrapePosts():
    
    try:
        post_button=WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CLASS_NAME, "_4xjz")))  # wait for page to be loaded (post option clickable)

        post_button.click()
        all_radios=driver.find_elements_by_css_selector('a._4f3b')
        
        for ar in all_radios:
        	ar_label=ar.find_element_by_css_selector('span._6ed5').text
        	if '2018' == ar_label:
        		radio_2018=ar.find_element_by_css_selector('label._55sh._1ka1')
        		radio_2018.click()
        		break
        # all videos
    #     yr2018_url = "https://www.facebook.com/search/str/%23airportroadaccident/keywords_blended_posts?f=Abobvb3j4FhnE06RPecwXXc845tnts3lrGLDQQOu1s7tSGzZ67-zk9DeXSKFYoeUSn9atpCsRpXZFR6VL0FP2_uFpzq4aKnLFtpC4mcY5gli0Z5pGWHO8eB3kQJpjIZ1yHD0A1ltXdN4VBjzq08Qxu74&epa=FILTERS&filters=eyJycF9hdXRob3IiOiJ7XCJuYW1lXCI6XCJteV9ncm91cHNfYW5kX3BhZ2VzX3Bvc3RzXCIsXCJhcmdzXCI6XCJcIn0iLCJycF9jcmVhdGlvbl90aW1lIjoie1wibmFtZVwiOlwiY3JlYXRpb25fdGltZVwiLFwiYXJnc1wiOlwie1xcXCJzdGFydF9tb250aFxcXCI6XFxcIjIwMTgtMDhcXFwiLFxcXCJlbmRfbW9udGhcXFwiOlxcXCIyMDE4LTA4XFxcIn1cIn0ifQ%3D%3D"
    #     driver.get(yr2018_url) # go to videos tab
    #     WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CLASS_NAME, "_4xjz")))  # wait till the page is loaded (posts option)
        
    #     # open a file to store image information
    #     f = open("post_gathered.txt", 'w', encoding='utf-8', newline='\r\n')
    #     f.writelines("post_link|posted by|post date|post time|like|sad|love|haha|wow|anger|comment|share\n")
        
    #     post_count = 0
    #     scroll()
            
    #     contents = driver.find_elements_by_class_name('_6rbb')  # post container class in search result
    #     print(len(contents))
    #     main_window = driver.current_window_handle # save main window
        
    #     for content in contents:
    #         line=""
    #         post_count = post_count + 1

    #         if post_count % 100 == 0:
    #             print(photo_count)
    #             time.sleep(270)

    #         elif post_count % 50 == 0:
    #             print(photo_count)
    #             time.sleep(150)

    #         elif post_count % 10 == 0:
    #             print(photo_count)
    #             time.sleep(60)

    #         post_link="xxxxxxxxxxxxxxx"
    #         posted_by="xxxxxxxxxxxxxxx"
    #         post_date="ddddddd"
    #         post_time="ttttttt"
    #         like_count="0"
    #         sad_count = "0"
    #         love_count = "0"
    #         haha_count = "0"
    #         wow_count = "0"
    #         angry_count = "0"
    #         comment="0"
    #         share="0"

                
    #         try:
    #             obj=content.find_element_by_class_name('_6-e6').find_element_by_tag_name('a').get_attribute('href')
    #             posted_by=obj[0: obj.find('?')]

    #         except:
    #             pass
                
    #         #print('posted by:', posted_by)
                
    #         try:
    #             obj=content.find_element_by_css_selector('span._6-cm').find_element_by_tag_name('a').text
    #             post_date=obj

    #         except:
    #             pass

    #         #print('post date: ', post_date)
                
                
    #         try:
    #             obj=content.find_element_by_css_selector('a._3hg-._42ft').text
    #             comment=obj[0: obj.find(' ')]

    #         except:
    #             pass

    #         #print('comments: ', comment)
                
                
    #         try:
    #             obj=content.find_element_by_css_selector('a._3rwx._42ft').text
    #             share=obj[0: obj.find(' ')]

    #         except:
    #             pass

    #         #print("shares: ", share)
                
                
                
    #         try:
    #             post_link=content.find_element_by_css_selector('span._6-cm').find_element_by_tag_name('a').get_attribute('href')
    #             driver.execute_script("window.open();") # open new blank tab
    #             driver.switch_to.window(driver.window_handles[1]) # switch focus to new window
    #             driver.get(post_link) # load the image in new window


    #             WebDriverWait(driver,30).until(EC.visibility_of_element_located((By.CLASS_NAME,"timestampContent")))
    #             obj=driver.find_element_by_css_selector('abbr._5ptz').get_attribute('title')
    #             post_time=obj[obj.find(' ')+1:]

    #             #print('post time: ', post_time)
                    
    #             try:

    #                 react_button=driver.find_element_by_css_selector("a._3dlf") # click reactions details pop up window
    #                 actions = ActionChains(driver)
    #                 actions.move_to_element(react_button).perform()
    #                 driver.execute_script("arguments[0].click();", react_button)

    #                 time.sleep(5)
    #                 # wait the pop up to open
    #                 close_button=WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a._42ft._5upp._50zy.layerCancel._1f6._51-t._50-0._50z-")))

    #                 reacs=driver.find_elements_by_css_selector('li._ds-._45hc')
    #                 for re in reacs:
    #                     lre=re.find_elements_by_tag_name("span")
    #                     for lr in lre:
    #                         tlr=lr.get_attribute("aria-label")

    #                         if tlr:
    #                             if 'Like' in tlr:
    #                                 like_count=tlr[0: tlr.find(' ')]

    #                             elif 'Sad' in tlr:
    #                                 sad_count=tlr[0: tlr.find(' ')]

    #                             elif 'Love' in tlr:
    #                                 love_count=tlr[0: tlr.find(' ')]

    #                             elif 'Wow' in tlr:
    #                                 wow_count=tlr[0: tlr.find(' ')]

    #                             elif 'Haha' in tlr:
    #                                 haha_count=tlr[0: tlr.find(' ')]

    #                             elif 'Angry' in tlr:
    #                                 angry_count=tlr[0: tlr.find(' ')]


    #                 close_button.click()

    #             except:
    #                 pass
                    
    #             #print('likes: ', like_count)
    #             #print('sad: ', sad_count)
    #             #print('love: ', love_count)
    #             #print('haha: ', haha_count)
    #             #print('wow: ', wow_count)
    #             #print('angry: ', angry_count)


    #             driver.close()
    #             driver.switch_to.window(main_window)
    #         except:
    #             print('error for post: ', post_count)
    #             exc_type = sys.exc_info()[0]
    #             exc_tb = sys.exc_info()[2]
    #             print(exc_type, exc_tb.tb_lineno)
    #             driver.close()
    #             driver.switch_to.window(main_window)
    #             pass

    #         line = post_link + "|" + posted_by + "|" + post_date + "|" + post_time + "|" + like_count + "|" + sad_count + "|" + love_count + "|" + haha_count + "|" + wow_count + "|" + angry_count + "|" + comment + "|" + share + "\n"
    #         f.writelines(line)

    #     f.close()

    except:
        exc_type = sys.exc_info()[0]
        exc_tb = sys.exc_info()[2]
        print(exc_type, exc_tb.tb_lineno)

        
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------


def scrapePhotos():

    try:
        element=WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.CLASS_NAME,"_4xjz"))) # wait for page to be loaded
        #all_url=driver.current_url
        #post_url=all_url.replace("top","posts")
        #post_url=post_url+"&epa=SERP_TAB" #go to posts tab to find all posts with particular hashtag
        #driver.get(post_url)
        
        #all photos from Aug 2018
        yr2018_url="https://www.facebook.com/search/str/%23wewantsaferoad/photos-keyword?f=AbrRMx3YuH9uV86Nser92wMYs3xglAXSdUxlE9XEu8xf0DPeMe7P1srwj94cQIBozDgE5TRg8VZMq1cPRi-PwlqaHkznqttXAo_8z5ekbYKZXC5mq4YjYKFihIMLOb5O8DE&epa=FILTERS&filters=eyJycF9jcmVhdGlvbl90aW1lIjoie1wibmFtZVwiOlwiY3JlYXRpb25fdGltZVwiLFwiYXJnc1wiOlwie1xcXCJzdGFydF9tb250aFxcXCI6XFxcIjIwMTgtMDdcXFwiLFxcXCJlbmRfbW9udGhcXFwiOlxcXCIyMDE4LTA3XFxcIn1cIn0ifQ%3D%3D"
        driver.get(yr2018_url)
        element=WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.CLASS_NAME,"_4xjz"))) #wait till the page is loaded (posts option)
        
        #open a file to store image information
        f = open("image_wewantjustice.txt", 'w', encoding='utf-8', newline='\r\n')
        f.writelines("image url|posted by|post date|post time|like|sad|love|haha|wow|anger|comment|share|location\n")
        
        scroll() #scroll the results page
        
        #get all images
        contents=driver.find_elements_by_class_name("_401d") # image container class in search result

        main_window = driver.current_window_handle # save main window
        photo_count=0
        print(len(contents))

        for content in contents: #for each image
            line=""
            try:

                image_link=content.find_element_by_css_selector('a').get_attribute('href') #get the image url
                driver.execute_script("window.open();") # open new blank tab
                driver.switch_to.window(driver.window_handles[1]) # switch focus to new window
                driver.get(image_link) # load the image in new window

                photo_count = photo_count + 1
                # wait so that we don't get tracked as bots
                if photo_count % 100 == 0:
                    print(photo_count)
                    time.sleep(270)

                elif photo_count % 50 == 0:
                    print(photo_count)
                    time.sleep(150)

                elif photo_count % 10 == 0:
                    print(photo_count)
                    time.sleep(60)

                line=line+image_link+"|"

                #wait for the image to be fully loaded (comment box)
                time.sleep(5)
                element=WebDriverWait(driver,30).until(EC.visibility_of_element_located((By.CLASS_NAME,"timestampContent")))

                #get user profile
                if "fbid" in image_link: # normal user
                    try:
                        user_profile=driver.find_element_by_class_name("profileLink")
                        posted_by=user_profile.get_attribute('href')

                    except:  # another kind of normal user
                        try:
                            user_profile = driver.find_element_by_css_selector("a._hli")
                            posted_by = user_profile.get_attribute('href')

                        except:
                            posted_by = "xxxxxxxxxxxxxxxxxxxxxxxx"
                            pass


                    #actual profile url upto ? mark
                    if posted_by.find('profile.php?id=')==-1:
                        qid=posted_by.find('?')
                        posted_by=posted_by[0:qid] #original url

                    else:
                        qid = posted_by.find('&')
                        posted_by = posted_by[0:qid]  # original url

                else: #photos posted by page
                    user_profile=driver.find_element_by_class_name("_64-f")
                    posted_by=user_profile.get_attribute('href')

                line=line+posted_by+"|"


                #get post date
                date_obj=driver.find_element_by_class_name("timestampContent")
                post_date=date_obj.text
                line=line+post_date+"|"

                #get post time
                post_time=driver.find_element_by_tag_name('abbr').get_attribute('title')
                #extract only the time portion
                colon=post_time.find(':')
                post_time=post_time[colon-2:colon+3]
                line=line+post_time+"|"


                #get total reaction count
                try:
                    tor=driver.find_element_by_class_name("_81hb").text
                    tor='i18n_reaction_count:"'+tor+'"'

                except:
                    pass

                #get reaction count: Like
                like_count="0"
                sad_count="0"
                love_count="0"
                haha_count="0"
                wow_count="0"
                angry_count = "0"

                react_soup=BeautifulSoup(requests.get(image_link).text, "html.parser")
                for scr in react_soup.find_all('script'):
                    if tor in scr.text:
                        #LIKE
                        like_id=scr.text.find('reaction_type:"LIKE"')
                        if like_id != -1:
                            st=scr.text[like_id:]
                            like_id=st.find('reaction_count:')
                            st=st[like_id:]
                            colon=st.find(':')
                            end=st.find('}')
                            like_count=st[colon+1:end]

                        #SORRY
                        sad_id = scr.text.find('reaction_type:"SORRY"')
                        if sad_id != -1:
                            st = scr.text[sad_id:]
                            sad_id = st.find('reaction_count:')
                            st = st[sad_id:]
                            colon = st.find(':')
                            end = st.find('}')
                            sad_count = st[colon + 1:end]

                        # LOVE
                        love_id = scr.text.find('reaction_type:"LOVE"')
                        if love_id!=-1:
                            st = scr.text[love_id:]
                            love_id = st.find('reaction_count:')
                            st = st[love_id:]
                            colon = st.find(':')
                            end = st.find('}')
                            love_count = st[colon + 1:end]

                        # HAHA
                        haha_id = scr.text.find('reaction_type:"HAHA"')
                        if haha_id!=-1:
                            st = scr.text[haha_id:]
                            haha_id = st.find('reaction_count:')
                            st = st[haha_id:]
                            colon = st.find(':')
                            end = st.find('}')
                            haha_count = st[colon + 1:end]

                        # WOW
                        wow_id = scr.text.find('reaction_type:"WOW"')
                        if wow_id!=-1:
                            st = scr.text[wow_id:]
                            wow_id = st.find('reaction_count:')
                            st = st[wow_id:]
                            colon = st.find(':')
                            end = st.find('}')
                            wow_count = st[colon + 1:end]

                        # ANGRY
                        angry_id = scr.text.find('reaction_type:"ANGER"')
                        if angry_id != -1:
                            st = scr.text[angry_id:]
                            angry_id = st.find('reaction_count:')
                            st = st[angry_id:]
                            colon = st.find(':')
                            end = st.find('}')
                            angry_count = st[colon + 1:end]

                        break

                line=line+like_count+"|"+sad_count+"|"+love_count+"|"+haha_count+"|"+wow_count+"|"+angry_count+"|"

                #comment
                try:
                    comment = driver.find_element_by_class_name("_6iij").find_element_by_css_selector('a._3hg-._42ft')
                    comment_count=comment.text
                    comment_count=comment_count[0: comment_count.find(" comment")]

                except:
                    comment_count="0"

                line=line+comment_count+"|"


                #share
                try:
                    share = driver.find_element_by_class_name("_6iij").find_element_by_css_selector('a._3rwx._42ft')
                    share_count=share.text
                    share_count=share_count[0: share_count.find(" share")]

                except:
                    share_count="0"

                line=line+share_count+"|"

                location = ""
                try:
                    location = driver.find_element_by_css_selector("a.taggee").text

                except:
                    pass
                
                line=line+location+"\n"

                f.writelines(line)

                driver.close()
                driver.switch_to.window(main_window)

            except (NoSuchElementException, StaleElementReferenceException, Exception) as e:
                estr="error for photo: "+str(photo_count)
                print(estr)

                #print error information
                exc_type = sys.exc_info()[0]
                exc_tb = sys.exc_info()[2]
                print(exc_type, exc_tb.tb_lineno)

                line=line+"error\n"
                f.writelines(line)

                driver.close()
                driver.switch_to.window(main_window)

                continue

        f.close()

    except Exception as e:
        print("Error finding photos!")
        print(sys.exc_info())
        exit()

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
        
def scrapeVideos():
    try:
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CLASS_NAME, "_4xjz")))  # wait for page to be loaded (post option clickable)

        # all videos
        yr2018_url = "https://www.facebook.com/search/videos/?q=%23we_want_justice&epa=FILTERS&filters=eyJycF9jcmVhdGlvbl90aW1lIjoie1wibmFtZVwiOlwiY3JlYXRpb25fdGltZVwiLFwiYXJnc1wiOlwie1xcXCJzdGFydF9tb250aFxcXCI6XFxcIjIwMTgtMDhcXFwiLFxcXCJlbmRfbW9udGhcXFwiOlxcXCIyMDE4LTA4XFxcIn1cIn0ifQ%3D%3D"
        driver.get(yr2018_url) # go to videos tab
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CLASS_NAME, "_4xjz")))  # wait till the page is loaded (posts option)
        
        # open a file to store image information
        f = open("video_wewantjustice.txt", 'w', encoding='utf-8', newline='\r\n')
        f.writelines("video url|posted by|post date|post time|like|sad|love|haha|wow|anger|view|comment|share\n")
        
        video_count = 0
        scroll()
            
        contents = driver.find_elements_by_css_selector('div._4ou3._6rnb')  # video container class in search result
        print(len(contents))
        
        driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)
        
        for content in contents:
            line=""
            video_count = video_count + 1
            try:
                #get post date and time
                
                obj=content.find_element_by_class_name("_42b-").find_element_by_css_selector('div.fsm.fwn.fcg')
                time_view=obj.find_element_by_tag_name('abbr').get_attribute('title')
                post_date=time_view[ time_view.find(",")+2: time_view.find(" at") ]
                post_time=time_view[ time_view.find(" at ")+4:] 
                print('post date:', post_date)
                print('post time:', post_time)
                
                #get view count
                post_view=obj.text[ obj.text.find("2018")+5 : obj.text.find('view')]
                post_view=post_view.replace(',','')
                post_view=post_view[2:]
                print('views: ', post_view)
                
                #get video url
                video_url=content.find_element_by_class_name("_14ax").find_element_by_tag_name("a").get_attribute("href")
                print('video url:', video_url)

                # click the video
                actions = ActionChains(driver)
                actions.move_to_element(content).perform()
                video_link=content.find_element_by_css_selector("a.async_saving._400z._2-40._33nl")
                driver.execute_script("arguments[0].click();", video_link)
      
                #backlink=WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "i.img.sp_S937Rx0Wce8.sx_388f22")))  # wait till the video is loaded (back option clickable)
                backlink = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "i.img.sp_HK2FO_Y2qQF.sx_9e04de")))
                time.sleep(5)
    
                # get number of comments
                try:
                    comment_count =  driver.find_element_by_css_selector('a._ipm._-56').text
                    comment_count = comment_count[0: comment_count.find(" Comment")]       
                except:
                    comment_count = "0"
                    pass
                
                print('comments: ', comment_count)
                
                # get number of shares
                try:
                    share_count = driver.find_element_by_css_selector('a._ipm._2x0m').text
                    share_count = share_count[0: share_count.find(" share")]
                    share_count=share_count.replace(',','')
    
                except:
                        share_count = "0"
                        pass
                    
                print('shares: ', share_count)

                like_count = "0"
                sad_count = "0"
                love_count = "0"
                haha_count = "0"
                wow_count = "0"
                angry_count = "0"
                
                #click on the reactions window
                try:
                    driver.find_element_by_class_name("_1g5v").click() # click reactions details pop up window

                    time.sleep(5)
                    # wait the pop up to open
                    close_button=WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a._42ft._5upp._50zy.layerCancel._1f6._51-t._50-0._50z-")))

                    reacs=driver.find_elements_by_css_selector('li._ds-._45hc')
                    for re in reacs:
                        lre=re.find_elements_by_tag_name("span")
                        for lr in lre:
                            tlr=lr.get_attribute("aria-label")

                            if tlr:
                                if 'Like' in tlr:
                                    like_count=tlr[0: tlr.find(' ')]

                                elif 'Sad' in tlr:
                                    sad_count=tlr[0: tlr.find(' ')]

                                elif 'Love' in tlr:
                                    love_count=tlr[0: tlr.find(' ')]

                                elif 'Wow' in tlr:
                                    wow_count=tlr[0: tlr.find(' ')]

                                elif 'Haha' in tlr:
                                    haha_count=tlr[0: tlr.find(' ')]

                                elif 'Angry' in tlr:
                                    angry_count=tlr[0: tlr.find(' ')]

                    close_button.click()  # close the pop up

                except:
                    pass
                            

                print('likes: ', like_count)
                print('sad: ', sad_count)
                print('love: ', love_count)
                print('haha: ', haha_count)
                print('wow: ', wow_count)
                print('angry: ', angry_count)
                
                #finally get user profile
                posted_by="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
                try:
                    posted_by=driver.find_element_by_css_selector("a._371y").get_attribute("href")
                    posted_by=posted_by[0: posted_by.find('?')]
                    
                except:
                    pass
                
                print('posted by:', posted_by)
                
                line=video_url+"|"+posted_by+"|"+post_date+"|"+post_time+"|"+like_count+"|"+sad_count+"|"+love_count+"|"+haha_count+"|"+wow_count+"|"+angry_count+"|"+post_view+"|"+comment_count+"|"+share_count+"\n";
                f.writelines(line)
                
                print('******************************')
                time.sleep(4)
                driver.back()
                time.sleep(5)
                
                #driver.execute_script("arguments[0].click();", backlink)
                
            except Exception as e:
    
                estr = "error for video: " + str(video_count)
                print(estr)
    
                # print error information
                exc_type = sys.exc_info()[0]
                exc_tb = sys.exc_info()[2]
                print(exc_type, exc_tb.tb_lineno)
                
                line=video_url+"|"+"|"+post_date+"|"+post_time+"|"+"|"+"|"+"|"+"|"+"|"+"|"+post_view+"|"+"|"+"errors\n"
                f.writelines(line)
    
                #backlink.click()
                
                continue
        
        f.close()
        
    except Exception as e:
        exc_type = sys.exc_info()[0]
        exc_tb = sys.exc_info()[2]
        print(exc_type, exc_tb.tb_lineno)
        exit()

# -------------------------------------------------------------
# -------------------------------------------------------------


def main():
    email = input('\nEnter your Facebook Email: ')
    password=getpass.getpass()


    login(email, password)
    searchKeyword()
    #scrapeVideos()
    scrapePosts()
# -------------------------------------------------------------
# -------------------------------------------------------------
# -------------------------------------------------------------

if __name__ == '__main__':
    # get things rolling
    main()