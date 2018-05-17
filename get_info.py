#!/usr/bin/python
import time
import re
from selenium import webdriver
from selenium.webdriver import FirefoxProfile, DesiredCapabilities
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import  expected_conditions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (
    ElementNotVisibleException
)
from selenium.webdriver.remote.webelement import WebElement
from  selenium.webdriver. common.action_chains import  ActionChains
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException, NoSuchWindowException
from config import DATABASE
host = DATABASE['host']
port = DATABASE['port']
enable_change_proxy = DATABASE['enable_change_proxy']

class function_webdriver():

    def __init__(self):
        self.profile = FirefoxProfile()
        self.profile.set_preference('permissions.default.desktop-notification', 1)
        if enable_change_proxy:
            self.profile = self.change_proxy(host, port, self.profile)
        else:
            self.profile = self.clear_proxy(self.profile)
        self.profile.update_preferences()
        self.driver = webdriver.Firefox(firefox_profile=self.profile)
        self.driver.maximize_window()

    def change_proxy(self, host, port, profile: object = None):
        if profile is None:
            profile = FirefoxProfile()
        profile.set_preference("network.proxy.type", 1)
        profile.set_preference("network.proxy.http", host)
        profile.set_preference("network.proxy.http_port", int(port))
        profile.set_preference("network.proxy.ssl", host)
        profile.set_preference("network.proxy.ssl_port", int(port))
        profile.update_preferences()
        return profile

    def clear_proxy(self, profile = None):
        if profile is None:
            profile = FirefoxProfile()
        profile.set_preference("network.proxy.type", 0)
        profile.update_preferences()
        return profile

    def login(self, user_name, password):
        print("Opened facebook")
        username_box = self.driver.find_element_by_id('email')
        username_box.send_keys(user_name)
        print("Email Id entered")
        time.sleep(1)
        password_box = self.driver.find_element_by_id('pass')
        password_box.send_keys(password)
        print("Password entered")
        login_box = self.driver.find_element_by_id('loginbutton')
        login_box.click()
        print("Done")
        return True

    def logout(self):
        logout = self.driver.find_element_by_id("userNavigationLabel")
        logout.click()
        time.sleep(1)
        logout2 = self.driver.find_element_by_css_selector(
            "li._54ni:nth-child(12) > a:nth-child(1) > span:nth-child(1) > span:nth-child(1)")
        logout2.click()
        return True

    def get_URL(self, url):        
        return self.driver.get(url)

    def quit(self):
        return self.clear_proxy(self.profile)

    #def wait_for_page_load(self):
    #    try:
    #        element_present = EC.presence_of_element_located((By.ID, "element_id"))
    #        WebDriverWait(self.driver, 10).until(element_present)
    #    except TimeoutException:
    #        print("Timed out waiting for page to load")

    def scroll_page(self):
        lenOfPage = self.driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        #self.wait_for_page_load()
        try:
            #element_present = EC.presence_of_element_located((By.ID, "element_id"))
            element_present = EC.presence_of_element_located((By.TAG_NAME, "html"))
            WebDriverWait(self.driver, 10).until(element_present)
        except TimeoutException:
            print("Timed out waiting for page to load")
        match = False
        while (match == False):
            lastCount = lenOfPage
            time.sleep(2)
            lenOfPage = self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
            if lastCount == lenOfPage:
                match = True

    def get_URL_image(self):
        images = self.driver.find_elements_by_css_selector("a[rel='theater'][data-render-location='homepage_stream']")
        #images = self.driver.find_elements_by_css_selector("a[class='_5pcq']")
        #images = self.driver.find_elements_by_class_name("_5pcq")
        for image in images:
            if ("video" in image.get_attribute("href")):
                continue
            str = image.get_attribute("href")
            print(str)
            self.click_Image(image)
            try:
                # element_present = EC.presence_of_element_located((By.ID, "element_id"))
                element_present = EC.presence_of_element_located((By.CLASS_NAME, "b=[spotlight]"))
                WebDriverWait(self.driver, 10).until(element_present)
            except TimeoutException:
                print("Timed out waiting for page to load")

            wait = WebDriverWait(self.driver,10)
            get_like_share = wait.until(EC.presence_of_element_located((By.ID, "fbPhotoSnowliftFeedback")))
            # Count the number of likes
            try:
                likes = get_like_share.find_element_by_class_name('_4arz')
            except NoSuchElementException as e:
                print("The number of likes: 0")
                pass
            else:
                number_of_likes = likes.get_attribute("innerText")
                print('The number of likes:', number_of_likes)
            # Count the number of shares
            try:
                shares = get_like_share.find_element_by_class_name('UFIShareLink')
            except (NoSuchElementException):
                print("The number of shares: 0")
                pass
            else:
                number_of_shares = shares.get_attribute("innerText")
                print('The number of shares:', number_of_shares)
        return image


    def click_Image(self, image):
        self.driver.execute_script("arguments[0].scrollIntoView(true);",image)
        self.driver.execute_script("arguments[0].click();",image)

'''
    def click_Image(self):
        child = self.driver.find_elements_by_css_selector("a[rel='theater']")
        child.click()
        for element in child:
            print(element)
            element.click()
            self.wait_for_page_load()
            element.send_keys(Keys.ESCAPE)
            self.wait_for_page_load()
'''


'''
#################################- This code will stop running after one time scroll -##################################
        SCROLL_PAUSE_TIME = 0.5
        # Get scroll height
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
        # Scroll down to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)
            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

########################################- This is a indefinte iteration -###############################################
    def scroll_page(self):
        self.body = self.driver.find_element_by_tag_name('body')
        while True:
            self.body.send_keys(Keys.PAGE_DOWN)



##############################- This code is also OK. However, it runs very slowly -####################################
        while self.driver.find_element_by_tag_name('div'):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            Divs = self.driver.find_element_by_tag_name('div').text
            if 'End of Results' in Divs:
                print ('end')
                break
            else:
                continue
'''
####################################################-execute-###########################################################
C = function_webdriver()
C.change_proxy(host, port)
C.get_URL('https://whoer.net')
C.get_URL('https://www.facebook.com')
user_name = DATABASE['user_name']
password = DATABASE['password']
C.login(user_name, password)
C.get_URL('https://www.facebook.com/search/str/i%20want%20this%20shirt/stories-keyword/today/date/stories/intersect')
C.scroll_page()
C.get_URL_image()
#C.logout()



