import os
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
from selenium.webdriver import FirefoxProfile, DesiredCapabilities
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

from .process_image import ProcessImage
from .utils import Utils
from config import DATABASE_CONFIG

# Process Image
path_image = DATABASE_CONFIG['pathImage']
tree_path = DATABASE_CONFIG['treePath']
enable_change_proxy = DATABASE_CONFIG['enable_change_proxy']
proxy_host = DATABASE_CONFIG['proxy_host']
proxy_port = DATABASE_CONFIG['proxy_port']

cur_path = os.path.dirname(__file__)
image_path_directory = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), path_image, tree_path)
if not os.path.exists(image_path_directory):
    os.makedirs(image_path_directory)

process_image = ProcessImage(image_path_directory)

class FunctionsWebDriver:
    def __init__(self, select_browser, tinydb_info_acc):
        self.select_browser = select_browser
        self.tinydb_info_acc = tinydb_info_acc
        self.profile: FirefoxProfile = FirefoxProfile()
        self.profile.set_preference("permissions.default.desktop-notification", 1)
        self.profile.set_preference("browser.download.folderList", 2)
        self.profile.set_preference("browser.download.manager.showWhenStarting", False)
        self.profile.set_preference("browser.download.dir", image_path_directory)
        self.profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/xml,text/plain,text/xml,"
                                                                              "image/jpeg image/png, text/csv")
        self.profile.set_preference("browser.helperApps.neverAsk.openFile", "application/xml,text/plain,text/xml,"
                                                                            "image/jpeg,image/png, text/csv")
        self.profile.set_preference("browser.helperApps.alwaysAsk.force", False)
        self.profile.set_preference("browser.download.manager.focusWhenStarting", False)
        self.profile.set_preference("browser.download.manager.useWindow", False)
        self.profile.set_preference("browser.download.manager.showAlertOnComplete", False)
        self.profile.set_preference("browser.download.manager.closeWhenDone", True)
        if enable_change_proxy:
            self.profile = self.change_proxy(proxy_host, proxy_port, self.profile)
        else:
            self.profile = self.clear_proxy(self.profile)
        self.profile.update_preferences()

        firefox_capabilities = DesiredCapabilities.FIREFOX
        firefox_capabilities['marionette'] = True
        firefox_capabilities['binary'] = '/usr/bin/firefox'

        self.web_driver = webdriver.Firefox(firefox_profile=self.profile, capabilities=firefox_capabilities)
        # self.web_driver1 = webdriver.Firefox(firefox_profile=self.profile, capabilities=firefox_capabilities)
        # self.web_driver2 = webdriver.Firefox(firefox_profile=self.profile, capabilities=firefox_capabilities)
        self.web_driver.maximize_window()
        self.actions = ActionChains(self.web_driver)

    def login(self, account_facebook):
        print("Opened facebook")
        username_box = self.web_driver.find_element_by_id('email')
        username_box.send_keys(account_facebook.username)
        print("Email Id entered")
        time.sleep(1)
        password_box = self.web_driver.find_element_by_id('pass')
        password_box.send_keys(account_facebook.password)
        print("Password entered")
        login_box = self.web_driver.find_element_by_id('loginbutton')
        login_box.click()
        print("Done")
        self.web_driver.get_screenshot_as_file("capture.png")
        return True

    @staticmethod
    def logout():
        return True

    def get_url(self, url):
        return self.web_driver.get(url)

    def quit(self):
        self.clear_proxy(self.profile)
        # self.web_driver.quit()

    def get_webdriver(self):
        return self.web_driver

    @staticmethod
    def change_proxy(ip_host: str, ip_port: str, profile: object = None) -> object:
        """
        Define Firefox Profile with you ProxyHost and ProxyPort
        
        :return: 
        :param ip_host: 
        :param ip_port: 
        :param profile: 
        :return: 
        """
        if profile is None:
            profile = FirefoxProfile()
        profile.set_preference("network.proxy.type", 1)
        profile.set_preference("network.proxy.http", ip_host)
        profile.set_preference("network.proxy.http_port", int(ip_port))
        profile.set_preference("network.proxy.ssl", ip_host)
        profile.set_preference("network.proxy.ssl_port", int(ip_port))
        profile.update_preferences()
        return profile

    @staticmethod
    def clear_proxy(profile=None):
        """

        :param profile:
        :return:
        """
        if profile is None:
            profile = FirefoxProfile()
        profile.set_preference("network.proxy.type", 0)
        profile.update_preferences()
        return profile

    def press_key_in_page_html(self, keypress: object) -> object:
        wait = WebDriverWait(self.web_driver, 10)
        search_page = wait.until(expected_conditions.presence_of_element_located((By.TAG_NAME, "html")))
        search_page.send_keys(keypress)
        return True

    def load_all_post_search(self):
        wait = WebDriverWait(self.web_driver, 10)
        search_page = wait.until(expected_conditions.presence_of_element_located((By.TAG_NAME, "html")))
        stop_send_key = False
        count = 100
        while not stop_send_key or count < 1:
            count -= 1
            search_page.send_keys(Keys.END)
            time.sleep(1)
            try:
                end_of_results_element = search_page.find_element_by_id('browse_end_of_results_footer')
                stop_send_key = True
            except NoSuchElementException as e:
                pass

    def click_see_more(self):
        list_see_more = self.web_driver.find_elements_by_class_name('see_more_link')
        for seeMore in list_see_more:
            seeMore.click()

    def get_name_container(self):
        count = 0
        timeout = 100
        condition_count = True
        list_name_container = ['BrowseResultsContainer', 'u_ps_0_3_0_browse_result_below_fold']
        while condition_count and timeout > 1:
            find_id = "fbBrowseScrollingPagerContainer" + str(count)
            timeout -= 1
            try:
                self.web_driver.find_element_by_id(find_id)
                list_name_container.append(find_id)
                count += 1
            except NoSuchElementException:
                condition_count = False
        return list_name_container

    def get_multiple_data_image_theater(self, type_script):
        if type_script == 1:
            [url, likes] = self.__get_faster__data_image_theater__()
        else:
            [url, likes] = self.__get__data_image_theater__()
        array_checkin = []
        array_checkin.extend(url)
        condition_out_while = True
        count = 50
        while condition_out_while and count > 0:
            count -= 1
            self.next_image_theater()
            if type_script == 1:
                [new_url, likes] = self.__get_faster__data_image_theater__()
            else:
                [new_url, likes] = self.__get__data_image_theater__()
            # check condition
            if new_url[0] in array_checkin:
                condition_out_while = False
            array_checkin.extend(new_url)
        return [array_checkin, likes]

    @property
    def get_different_data_image(self) -> object:
        try:
            array_url = []
            wait = WebDriverWait(self.web_driver, 10)
            element_multi_image = wait.until(expected_conditions.presence_of_element_located((
                By.CSS_SELECTOR, 'divclass=\'_10 _1mlf uiLayer _4-hy _3qw\']')))
            all_image = wait.until(expected_conditions.presence_of_all_elements_located((By.CLASS_NAME, "_580_")))
            for image in all_image:
                url = image.get_attribute('src')
                name_image = Utils.get_name_in_string()
                process_image.get_image_from_url(url, name_image)
                array_url.append(url)
            like = '0'
            return [array_url, like]
        finally:
            return [[], '0']

    def get_like_share_in_post(self, child_user_content_wrapper, default_likes=0):
        try:
            like_comment_content_element = child_user_content_wrapper.find_element_by_class_name('commentable_item')
            # Ta on bai post bang cach like
            button_like_post = like_comment_content_element.find_elements_by_class_name("UFILikeLink")
            if button_like_post.__len__() > 0:
                for button in button_like_post:
                    try:
                        button.click()
                    finally:  # ignore
                        pass
            text_like = self._get_like_comment_share(like_comment_content_element, default_likes)
            return text_like
        except NoSuchElementException as e:
            return '{0} like, comment, share'.format(str(default_likes))

    def _get_like_comment_share(self, element, default_like=None):
        text = ""
        array = []
        if default_like is None:
            likes = element.find_elements_by_class_name('_4arz')
            for like in likes:
                text += like.text + ' likes, '
                array.extend(Utils.get_numbers_in_string())
        else:
            text += str(default_like) + ' likes, '
            array.extend([default_like])
        comment_shares = element.find_elements_by_class_name('_36_q')
        for comment_share in comment_shares:
            text += comment_share.text + ', '
            array.extend(Utils.get_numbers_in_string())
        if text == "":
            text = "None like,comment,share"
        return text

    def _click_first_image_theater_(self, image_element):
        self.web_driver.execute_script("arguments[0].scrollIntoView();", image_element)
        self.web_driver.execute_script("arguments[0].click();", image_element)
        time.sleep(1)

    def function_for__data_image_theater(self):
        wait = WebDriverWait(self.web_driver, 10)
        likes = None
        element = wait.until(expected_conditions.presence_of_element_located((By.ID, "photos_snowlift")))
        dropdown_button = wait.until(
            expected_conditions.presence_of_element_located((By.CLASS_NAME, "fbPhotoSnowliftDropdownButton")))
        dropdown_button.click()
        div_download_not_hidden = wait.until(
            expected_conditions.presence_of_element_located(
                (By.CSS_SELECTOR, "div.uiContextualLayerPositioner:not(.hidden_elem)")))
        wait_download = WebDriverWait(div_download_not_hidden, 10)
        image_urls_download = wait_download.until(
            expected_conditions.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "a[data-action-type='download_photo']")))
        if image_urls_download.__len__() == 0:
            url = ''
        else:
            url = image_urls_download[0].get_attribute('href')
            image_urls_download[0].click()
        likes = '0'
        feedback_element = wait.until(
            expected_conditions.presence_of_element_located((By.ID, 'fbPhotoSnowliftFeedback')))
        try:
            likes = feedback_element.find_element_by_class_name("_4arz").text
        finally:
            pass
        dropdown_button.click()
        return [url, likes]

    def __get__data_image_theater__(self):
        try:
            [url, likes] = self.function_for__data_image_theater()
        except StaleElementReferenceException as e:
            print(e)
            time.sleep(1)
            [url, likes] = self.function_for__data_image_theater()
        return [url, likes]

    def function_for_faster__data_image_theater(self):
        try:
            wait = WebDriverWait(self.web_driver, 10)
            likes = None
            element_theater = wait.until(expected_conditions.presence_of_element_located((By.ID, "photos_snowlift")))

            # Check dopdown button
            dropdown_button = wait.until(
                expected_conditions.presence_of_element_located((By.CLASS_NAME, "fbPhotoSnowliftDropdownButton")))

            element = wait.until(expected_conditions.presence_of_element_located((By.CLASS_NAME, "stageWrapper")))

            image_urls_download = wait.until(
                element.presence_of_all_elements_located((By.CSS_SELECTOR, "img[class='spotlight']")))
            if image_urls_download.__len__() == 0:
                url = ''
            else:
                url = image_urls_download[0].get_attribute('src')
                name_image = Utils.get_name_in_string()
                process_image.get_image_from_url(url, name_image)
            likes = '0'
            feedback_element = wait.until(
                expected_conditions.presence_of_element_located((By.ID, 'fbPhotoSnowliftFeedback')))
            try:
                likes = feedback_element.find_element_by_class_name("_4arz").text
            except:
                pass
        except TimeoutException as e:
            # Check video once
            pass
        except:
            pass
        return [[url], likes]

    def __get_faster__data_image_theater__(self):
        try:
            [url, likes] = self.function_for_faster__data_image_theater()
        except StaleElementReferenceException as e:
            print(e)
            time.sleep(2)
            [url, likes] = self.function_for_faster__data_image_theater()
        return [url, likes]

    def escape_theater(self):
        self.press_key_in_page_html(Keys.ESCAPE)
        # Check Complete escape
        find_escape = self.web_driver.find_elements_by_class_name("_xlt")
        find_escape1 = self.web_driver.find_elements_by_class_name("layerCancel")
        if find_escape.__len__() > 0 or find_escape1.__len__() > 0:
            self.press_key_in_page_html(Keys.ESCAPE)

    def next_image_theater(self):
        self.press_key_in_page_html(Keys.ARROW_RIGHT)
        time.sleep(1)  # wait load page

    def get_data_container(self, name: str, type_script: object) -> object:
        """

        :param name:
        :param type_script:
        :return:
        """
        try:
            browse_results_container = self.web_driver.find_element_by_id(name)
        except NoSuchElementException:
            return 0
        childes_user_content_wrapper = browse_results_container.find_elements_by_class_name('userContentWrapper')
        for child_user_content_wrapper in childes_user_content_wrapper:
            try:
                self.get_data_content_wrapper(child_user_content_wrapper, type_script)
            finally:
                pass

    def get_data_content_wrapper(self, child_user_content_wrapper, type_script):
        self.web_driver.execute_script("arguments[0].scrollIntoView(true);", child_user_content_wrapper)
        print('<-------------------->')
        content_post = ""
        try:
            content_post = child_user_content_wrapper.find_element_by_class_name(   'userContent').text
        except NoSuchElementException as e:
            content_post = 'Empty Content'
        # Get Image URL
        list_image_url = child_user_content_wrapper.find_elements_by_css_selector(
            "a[rel='theater'][data-render-location='homepage_stream']")
        if list_image_url.__len__() == 0:
            print('No Image')

        if list_image_url.__len__() == 1:
            url = []
            likes = None
            likes = self.get_like_share_in_post(child_user_content_wrapper)
            self._click_first_image_theater_(list_image_url[0])
            try:
                if type_script == 1:
                    [url, likes] = self.__get_faster__data_image_theater__()
                else:
                    [url, likes] = self.__get__data_image_theater__()
            except TimeoutException as e:
                print('dac biet')
                [url, likes] = self.get_different_data_image
            # update likes
            print(url)
            self.tinydb_info_acc.insert(content_post, likes, url)

        if list_image_url.__len__() > 1:
            likes = self.get_like_share_in_post(child_user_content_wrapper)
            self._click_first_image_theater_(list_image_url[0])
            try:
                [url, like] = self.get_multiple_data_image_theater(type_script)
            except TimeoutException as e:
                print('dac biet')
                [url, like] = self.get_different_data_image
            print(url)
            self.tinydb_info_acc.insert(content_post, likes, url)
        self.escape_theater()

    def add_cookie(self):
        pass

    def likepostActivity(self):
        pass
