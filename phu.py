#!/usr/bin/python
import time
from selenium import webdriver
from selenium.webdriver import FirefoxProfile
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait as wait
from PIL import Image, ImageFont, ImageDraw, ImageOps
from selenium.webdriver.common.alert import Alert
import requests
import os
os.path.exists('/Users/paul/Library/Fonts/Verdana.ttf')
from config import DATABASE

proxy_host = DATABASE['proxy_host']
proxy_port = DATABASE['proxy_port']
enable_change_proxy = DATABASE['enable_change_proxy']
username_proxy = DATABASE['username_proxy']
password_proxy = DATABASE['password_proxy']
#textSearch = DATABASE['textSearch']

class functionwebdriver():
    def __init__(self):
        self.profile = FirefoxProfile()
        self.profile.set_preference('permissions.default.desktop-notification', 1)
        if enable_change_proxy:
            self.profile = self.change_proxy(proxy_host, proxy_port, self.profile)
        else:
            self.profile = self.clear_proxy(self.profile)
        self.profile.update_preferences()
        self.driver = webdriver.Firefox(firefox_profile=self.profile)
        #self.driver.maximize_window()


    def change_proxy(self, proxy_host, proxy_port, profile: object = None):
        if profile is None:
            profile = FirefoxProfile()
        profile.set_preference("network.proxy.type", 1)
        profile.set_preference("network.proxy.http", proxy_host)
        profile.set_preference("network.proxy.http_port", int(proxy_port))
        profile.set_preference("network.proxy.ssl", proxy_host)
        profile.set_preference("network.proxy.ssl_port", int(proxy_port))
        profile.update_preferences()
        return profile

    def authentication_proxy(self, username_proxy, password_proxy):
        wait(self.driver, 3).until(EC.alert_is_present())
        alert = self.driver.switch_to.alert
        alert.send_keys(username_proxy + Keys.TAB + password_proxy)
        alert.accept()
        self.driver.get('https://whoer.net')

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
        #self.driver.get(url)
        return self.driver.get(url)

    def load(self):
        self.driver.get('https://www.facebook.com')

    def quit(self):
        return self.clear_proxy(self.profile)

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

    def get_like_share(self):
        wait = WebDriverWait(self.driver, 1)
        feedbackElement = wait.until(EC.presence_of_element_located((By.ID, "fbPhotoSnowliftFeedback")))
        '''
        try:
            element_present = EC.presence_of_element_located((By.CLASS_NAME, "b=[spotlight]"))
            WebDriverWait(self.driver, 10).until(element_present)
        except TimeoutException:
            pass
            #print("Timed out waiting for page to load")
        '''
        # Count the number of likes
        try:
            likes = feedbackElement.find_element_by_class_name('_4arz')
        except (NoSuchElementException):
            number_of_likes = '0'
            print("The number of likes: 0")
            pass
        else:
            number_of_likes = likes.get_attribute("innerText")
            # numbers_of_likes = likes.text
            print('The number of likes:', number_of_likes)
        # Count the number of shares
        try:
            shares = feedbackElement.find_element_by_class_name('UFIShareLink')
        except (NoSuchElementException):
            number_of_shares = '0'
            print("The number of shares: 0")
            pass
        else:
            number_of_shares = shares.get_attribute("innerText")
            print('The number of shares:', number_of_shares)
        return number_of_likes, number_of_shares


    def get_info_image(self):# , file_out
        posts = self.driver.find_elements_by_class_name("userContentWrapper")  # class name of post
        img = []
        index_image = 0
        for post in posts:
            images = post.find_elements_by_css_selector("a[rel='theater'][data-render-location='homepage_stream']")
            # permalink
            if (len(images) == 0):
                print("There is no image")

            if (len(images) == 1):
                if ("video" in images[0].get_attribute("href")):
                    continue
                self.driver.execute_script("arguments[0].click();", images[0])
                try:
                    element_present = EC.presence_of_element_located((By.CLASS_NAME, "b=[spotlight]"))
                    WebDriverWait(self.driver, 10).until(element_present)
                except TimeoutException:
                    print("Timed out waiting for page to load")

                #images[0], self.driver.current_url
                if (self.driver.current_url == 'https://www.facebook.com/search/str/i%20want%20this%20shirt/stories-keyword/today/date/stories/intersect'):
                    continue
                print(self.driver.current_url)
                number_of_likes, number_of_shares = self.get_like_share()

                index_image = index_image + 1
                down_image = self.download_image(index_image, number_of_likes, number_of_shares)  # file_out
                img.append(down_image)
                pass
                images[0].send_keys(Keys.ESCAPE)

            if (len(images) > 1):
                i = 0
                url = []
                self.driver.execute_script("arguments[0].click();", images[0])
                try:
                    element_present = EC.presence_of_element_located((By.CLASS_NAME, "b=[spotlight]"))
                    WebDriverWait(self.driver, 5).until(element_present)
                except TimeoutException:
                    print("Timed out waiting for page to load")
                if (self.driver.current_url == 'https://www.facebook.com/search/str/i%20want%20this%20shirt/stories-keyword/today/date/stories/intersect'):
                    continue
                #element_present, self.driver.current_url
                url.append(self.driver.current_url)
                print(url[0])
                number_of_likes, number_of_shares = self.get_like_share()

                index_image = index_image + 1
                down_image = self.download_image(index_image, number_of_likes, number_of_shares)  # file_out
                img.append(down_image)
                while (True):
                    i = i + 1
                    wait = WebDriverWait(self.driver, 10)
                    click_next = wait.until(EC.presence_of_element_located((By.TAG_NAME, "html")))
                    click_next.send_keys(Keys.ARROW_RIGHT)

                    try:
                        element_present = EC.presence_of_element_located((By.CLASS_NAME, "b=[spotlight]"))
                        WebDriverWait(self.driver, 10).until(element_present)
                    except TimeoutException:
                        print("Timed out waiting for page to load")
                    url.append(self.driver.current_url)
                    print(url[i])
                    number_of_likes, number_of_shares = self.get_like_share()

                    index_image = index_image + 1
                    down_image = self.download_image(index_image, number_of_likes, number_of_shares)  # file_out
                    img.append(down_image)
                    if (url[i] == url[0]):
                        break
                click_next.send_keys(Keys.ESCAPE)
        print(len(img))
        return True

    def click_Image(self, image):
        self.driver.execute_script("arguments[0].scrollIntoView(true);",image)
        self.driver.execute_script("arguments[0].click();",image)

    def download_image(self,index_image, number_of_likes, number_of_shares):#
        image_attri = self.driver.find_element_by_class_name('spotlight')
        src_image = image_attri.get_attribute('src')
        print(src_image)
        down_image = requests.get(src_image)
        with open('image'+'_'+str(index_image)+'.jpg','wb+') as write_image:#+'.jpg'
            write_image.write(down_image.content)
            read_image = Image.open(write_image)
            font_type = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeMono.ttf", 40, encoding="unica")
            read_image_with_border = ImageOps.expand(read_image,border=200,fill='black')
            draw = ImageDraw.Draw(read_image_with_border)
            #draw.rectangle(((0, 0), (200, 200)), fill="black", outline="blue")
            draw.text(xy=(400,150),text=number_of_likes+' '+'likes'+' '+number_of_shares,fill=(255,255,255),font=font_type)
            read_image_with_border.save('image'+'_'+str(index_image)+'.jpg')
            #read_image.show()
        return down_image

    def send_message(self):
        self.get_URL('https://www.facebook.com/lnanhkhoa')
        #message_box = self.driver.find_element_by_css_selector("a[href='https://www.facebook.com/messages/t/100004703621008']")
        message_box = self.driver.find_element_by_css_selector("a[href='/messages/t/lnanhkhoa/']")
        message_box.click()
        time.sleep(5)
        send_box = self.driver.find_element_by_css_selector(".notranslate")
        #time.sleep(10)
        send_box.send_keys("Hi")
        send_box.send_keys(Keys.ENTER)

####################################################-execute-###########################################################
#C = functionwebdriver()
#C.change_proxy(proxy_host, proxy_port)
#C.authentication_proxy(username_proxy, password_proxy)
#C.get_URL('https://www.facebook.com')
#user_name = DATABASE['user_name']
#password = DATABASE['password']
#C.login(user_name, password)
#C.send_message()
#search_page = function_webdriver.get_URL('https://www.facebook.com/search/str/' + textSearch + '/stories-keyword/today/date/stories/intersect')
#C.get_URL('https://www.facebook.com/search/str/i%20want%20this%20shirt/stories-keyword/today/date/stories/intersect')
#C.scroll_page()
#C.get_info_image()
#C.logout()
#C.quit()

