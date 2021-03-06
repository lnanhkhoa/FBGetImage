import os
import time
import random
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
from selenium.webdriver import FirefoxProfile, DesiredCapabilities
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options

from .process_image import ProcessImage
from apps.utils import Utils
from config import DATABASE_CONFIG
from manager_files import *

# Process Image
path_image = DATABASE_CONFIG['path_image']
enable_change_proxy = DATABASE_CONFIG['enable_change_proxy']
type_script = DATABASE_CONFIG['type_of_run_script']
cur_path = os.path.dirname(__file__)


class FunctionsWebDriver:
    def __init__(self, select_browser, tinydb_info_acc, numeric):
        tree_path = str(numeric)
        image_path_directory = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                            path_image, tree_path)
        all_images_path_directory = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                                 path_image, "all")
        if not os.path.exists(image_path_directory):
            os.makedirs(image_path_directory)
        if not os.path.exists(all_images_path_directory):
            os.makedirs(all_images_path_directory)

        self.process_image = ProcessImage(tree_path, image_path_directory, all_images_path_directory)
        self.select_browser = select_browser
        self.tinydb_info_acc = tinydb_info_acc
        self.authentication = False
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

        text_proxy = get_proxy(numeric)
        array_proxy = text_proxy.split('|')
        if array_proxy.__len__() > 3:
            necessary_authen = True
            proxy_host = array_proxy[0]
            proxy_port = array_proxy[1]
            proxy_authen = dict(
                username=array_proxy[2],
                password=array_proxy[3]
            )
        else:
            necessary_authen = False
            proxy_host = array_proxy[0]
            proxy_port = array_proxy[1]
            proxy_authen = dict()

        if enable_change_proxy == '1':
            self.profile = self.change_proxy(proxy_host, proxy_port, self.profile)
        else:
            self.profile = self.clear_proxy(self.profile)
        self.profile.update_preferences()
        #
        # firefox_capabilities = DesiredCapabilities.FIREFOX
        # firefox_capabilities['marionette'] = True
        # firefox_capabilities['binary'] = '/usr/bin/firefox'

        options = Options()
        options.add_argument("--headless")
        self.web_driver = webdriver.Firefox(firefox_profile=self.profile, firefox_options=options)
        if necessary_authen:
            self.authentication = self.handling_authentication(proxy_authen)
        # self.web_driver.maximize_window()
        self.actions = ActionChains(self.web_driver)

    def is_authen(self):
        return self.authentication

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

    """
        Here is functions for mini-task        
    """

    def login(self, account_facebook):
        print("Opened facebook")
        try:
            username_box = self.web_driver.find_element_by_id('email')
            username_box.send_keys(account_facebook.username)
            time.sleep(0.5)
            password_box = self.web_driver.find_element_by_id('pass')
            password_box.send_keys(account_facebook.password)
            login_box = self.web_driver.find_element_by_id('loginbutton')
            login_box.click()
            print("Login Successfully !")
            return True
        except Exception as e:
            print('error in Login')
            return False
    def logout(self):
        try:
            logout = self.web_driver.find_element_by_id("userNavigationLabel")
            logout.click()
            print('log out acc')
            time.sleep(3)
            logout2 = self.web_driver.find_element_by_css_selector(
                "li._54ni:nth-child(12) > a:nth-child(1) > span:nth-child(1) > span:nth-child(1)")
            logout2.click()
        except Exception as e:
            print("-->Error in Logout: ")
            print(e)

    def press_key_in_page_html(self, keypress: object) -> object:
        wait = WebDriverWait(self.web_driver, 10)
        search_page = wait.until(expected_conditions.presence_of_element_located((By.TAG_NAME, "html")))
        search_page.send_keys(keypress)
        return True

    def load_all_post_search(self):
        wait = WebDriverWait(self.web_driver, 10)
        search_page = wait.until(expected_conditions.presence_of_element_located((By.TAG_NAME, "html")))
        stop_send_key = False
        count = 50
        while not (stop_send_key or count < 1):
            count -= 1
            search_page.send_keys(Keys.END)
            time.sleep(2)
            try:
                search_page.find_element_by_id('browse_end_of_results_footer')
                stop_send_key = True
            except NoSuchElementException as e:
                pass
            except:
                pass
        print('load All Done')

    def click_see_more(self):
        print("click_see_more")
        list_see_more = self.web_driver.find_elements_by_class_name('see_more_link')
        for seeMore in list_see_more:
            try:
                seeMore.click()
            except Exception as e:
                print('error in click_see_more')
                print(e)

    def check_checkpoint(self):
        try:
            self.web_driver.find_element_by_class_name('BrowseResultsContainer')
            self.web_driver.find_element_by_class_name('u_ps_0_3_0_browse_result_below_fold')
            return False
        except:
            return True

    def get_list_name_container(self):
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
            except:
                print("Error in get listname container")
        return list_name_container

    def _click_first_image_theater_(self, image_element):
        try:
            self.web_driver.execute_script("arguments[0].scrollIntoView();", image_element)
            self.web_driver.execute_script("arguments[0].click();", image_element)
            time.sleep(2)
        except:
            raise Exception("Error when click image")

    def escape_theater(self):
        self.press_key_in_page_html(Keys.ESCAPE)
        # Check Complete escape
        find_escape = self.web_driver.find_elements_by_class_name("_xlt")
        find_escape1 = self.web_driver.find_elements_by_class_name("layerCancel")
        if find_escape.__len__() > 0 or find_escape1.__len__() > 0:
            self.press_key_in_page_html(Keys.ESCAPE)

    def next_image_theater(self):
        self.press_key_in_page_html(Keys.ARROW_RIGHT)
        time.sleep(0.5)  # wait load page

    def get_url(self, url):
        return self.web_driver.get(url)

    def scroll_into_view_by_js(self, object: object):
        self.web_driver.execute_script("arguments[0].scrollIntoView(true);", object)

    def like_the_post(self, element_wrapper):
        # Ta on bai post bang cach like
        time.sleep(0.2)
        try:
            like_comment_content_element = element_wrapper.find_element_by_class_name('commentable_item')
            like_comment_content_element_next = like_comment_content_element.find_element_by_class_name('_37uu')
            button_like_post = like_comment_content_element_next.find_elements_by_class_name("UFILikeLink")
            if button_like_post.__len__() > 0:
                button_like_post[0].click()
                print("like ta on")
        except:  # ignore
            print("khong like dc, khong like dc thi thoi")
            pass

    def quit(self):
        self.clear_proxy(self.profile)
        self.web_driver.quit()

    def get_webdriver(self):
        return self.web_driver

    def process_in_container(self, name: str):
        """
        :param name:
        :return:
        """
        try:
            browse_results_container = self.web_driver.find_element_by_id(name)
            childes_user_content_wrapper = browse_results_container.find_elements_by_class_name('userContentWrapper')
            for child_user_content_wrapper in childes_user_content_wrapper:
                try:
                    self.process_in_post(child_user_content_wrapper)
                except Exception as e:
                    print(e)
                    print("Error in post")
        except NoSuchElementException as e:
            print('NoSuchElementException', e)
        except:
            print("Error in container")

    def process_in_post(self, child_user_content_wrapper):
        """
         - Get content of post
         - Classify and get likes-share-comment
         - Like post
         - Save link in content of post

        :param child_user_content_wrapper:
        :return:
        """
        self.scroll_into_view_by_js(child_user_content_wrapper)
        print('<-------------------->')
        content_post = self.get_content_of_post(child_user_content_wrapper)
        list_link = Utils.get_link_buy_product(content_post)
        self.save_link_to_buy_product(list_link)  # skip
        list_image_urls = self.process_get_images_in_post(child_user_content_wrapper)
        print(len(list_image_urls), list_image_urls)
        # self.like_the_post(child_user_content_wrapper)

    def get_content_of_post(self, element_wapper):
        try:
            content_post = element_wapper.find_element_by_class_name('userContent').text
        except NoSuchElementException as e:
            content_post = 'Empty Content'
        except:
            content_post = ''
        return content_post

    def save_link_to_buy_product(self, list_link):
        pass

    def process_get_images_in_post(self, element_wapper):
        """
        :param element_wapper:
        :return list image urls
        """
        list_image_urls = []
        list_image_theater = element_wapper.find_elements_by_css_selector("a[rel='theater']"
                                                                          + "[data-render-location='homepage_stream']")
        if list_image_theater.__len__() == 0:
            print("No image")
            list_image_urls = []
            pass

        if list_image_theater.__len__() == 1:
            """
                In one image, getting like, share when click to show theater image
            """
            print("Just 1 image")
            self._click_first_image_theater_(list_image_theater[0])
            url = []
            likes = ''
            result_tracking = self.tracking_theater()
            if result_tracking == 1:
                if type_script == '1':
                    [list_image_urls, likes] = self.__get_faster__data_image_theater__()
            if result_tracking == 3:
                [list_image_urls, likes] = self.get_different_data_image()
            # update likes
            # self.tinydb_info_acc.insert(content_post, likes, url)

        if list_image_theater.__len__() > 1:
            print(">1 images")
            self._click_first_image_theater_(list_image_theater[0])
            # likes = self.get_like_share_in_post(child_user_content_wrapper)
            likes = '0'
            [list_image_urls, like] = self.get_multiple_data_image_theater()
            # self.tinydb_info_acc.insert(content_post, likes, list_image_urls)
        self.escape_theater()
        return list_image_urls

    def get_like_in_post(self, element_wrapper):
        pass

    def get_like_in_theater(self):
        wait = WebDriverWait(self.web_driver, 10)
        get_like_share = wait.until(expected_conditions.presence_of_element_located((By.ID, "fbPhotoSnowliftFeedback")))
        # Count the number of likes
        number_of_likes, number_of_shares = '0 likes', '0 share'
        try:
            likes = get_like_share.find_element_by_class_name('_4arz')
            likes_text = likes.get_attribute("innerText")
            if likes_text.find('likes') > 0:
                likes_text += ' likes'
        except NoSuchElementException as e:
            pass
        except Exception as e:
            print(e)
        # Count the number of shares
        try:
            shares = get_like_share.find_element_by_class_name('UFIShareLink')
            number_of_shares = shares.get_attribute("innerText")
        except NoSuchElementException:
            pass
        except Exception as e:
            print(e)
        return str(number_of_likes + ', ' + number_of_shares)

    def tracking_theater(self):
        """
        track:
        image, video or difference
        :return: 1 image, 2 video, 3 difference
        """
        wait = WebDriverWait(self.web_driver, 5)
        wait1s = WebDriverWait(self.web_driver, 5)
        try:
            element_theater = wait.until(expected_conditions.presence_of_element_located((By.ID, "photos_snowlift")))

            # Check dopdown button
            wait.until(
                expected_conditions.presence_of_element_located((By.CLASS_NAME, "fbPhotoSnowliftDropdownButton")))
            div_stage = wait.until(expected_conditions.presence_of_element_located((By.CLASS_NAME, "stageWrapper")))
            div_image = wait1s.until(expected_conditions.presence_of_element_located(
                (By.CSS_SELECTOR, "div._2-sx:not(.hidden_elem)")))
            image_urls_download = div_image.find_elements_by_class_name("spotlight")
            print('done tracking')
            return 1
        except TimeoutException as e:
            # Check video once
            try:
                wait1s.until(expected_conditions.presence_of_element_located((By.CLASS_NAME, "showVideo")))
                print('this is video, next theater')
                return 2
            except:
                print('After check video')
                return 3
        except Exception as e:
            print(e)
            print('None tracking')
            return 3

    def function_for_faster_data_image_theater(self):
        """
            get image
            track:
                image, video or difference
        :rtype: object
            :return:
        """
        wait = WebDriverWait(self.web_driver, 5)
        div_image = wait.until(expected_conditions.presence_of_element_located(
            (By.CLASS_NAME, "stageWrapper")))
        image_urls_download = div_image.find_elements_by_class_name("spotlight")
        like_share = self.get_like_in_theater()
        if image_urls_download.__len__() == 0:
            url = ""
        else:
            url = image_urls_download[0].get_attribute('src')
            if '.jpg' in url:
                name_image = Utils.get_name_in_string(url)
                self.process_image.get_image_from_url(url, name_image)
                self.process_image.get_image_into_all(url, name_image)
                self.process_image.add_likes_shares_into_image(name_image, like_share)
            else:
                url = ""
        return [[url], like_share]

    def __get_faster__data_image_theater__(self):
        # try:
        [url, likes] = self.function_for_faster_data_image_theater()
        # except StaleElementReferenceException as e:
        #     print(e)
        #     time.sleep(2)
        #     [url, likes] = self.function_for_faster_data_image_theater(objects)
        return [url, likes]

    def get_multiple_data_image_theater(self):
        print('multi mode')
        array_checkin = []
        array_likeshare = []
        result_tracking_post = self.tracking_theater()
        if result_tracking_post == 3:
            # mac dinh 0 likes, 0 share
            [array_checkin, likes] = self.get_different_data_image()
            return [array_checkin, likes]
        # have many images
        result_tracking = result_tracking_post
        for x in range(0, 50):
            if result_tracking == 1:
                if type_script == '1':
                    [new_url, likes] = self.__get_faster__data_image_theater__()
                    if new_url[0] in array_checkin:
                        break
                    array_checkin.extend(new_url)
                    array_likeshare.append(likes)
            self.next_image_theater()
            result_tracking = self.tracking_theater()
        print(array_likeshare)
        return [array_checkin, likes]

    def get_different_data_image(self) -> object:
        print('dac biet')
        try:
            array_url = []
            wait = WebDriverWait(self.web_driver, 5)
            wait.until(expected_conditions.presence_of_element_located((
                By.CSS_SELECTOR, "div[class='_10 _1mlf uiLayer _4-hy _3qw']")))
            all_image = wait.until(expected_conditions.presence_of_all_elements_located((By.CLASS_NAME, "_580_")))
            like_share = '0 likes, 0 shares'
            for image in all_image:
                url = image.get_attribute('src')
                if '.jpg' in url:
                    name_image = Utils.get_name_in_string(url)
                    self.process_image.get_image_from_url(url, name_image)
                    self.process_image.get_image_into_all(url, name_image)
                    self.process_image.add_likes_shares_into_image(name_image, like_share)
                    array_url.append(url)
            return [array_url, like_share]
        except Exception as e:
            print(e)
            print("error when get diff image")
            return [[], '0']

    def function_like_fanpage(self, percent):
        list_likepage_button = self.web_driver.find_elements_by_css_selector(
            'button.PageLikeButton:not(PageLikedButton)')
        length = list_likepage_button.__len__()
        number_of_delete_elements = Utils.holding_percent(length, percent)
        print('like fanpage ' + str(length - number_of_delete_elements)
              + '/ ' + str(length))
        if number_of_delete_elements > 0:
            for x in range(0, number_of_delete_elements):
                list_likepage_button.pop(random.randint(0, length - x - 1))
        if list_likepage_button.__len__() > 0:
            for likepage_button in list_likepage_button:
                # avoid Stale Element Exception
                id = likepage_button.get_attribute('id')
                button = self.web_driver.find_element_by_id(id)
                self.web_driver.execute_script("arguments[0].click();", button)
                time.sleep(1)

    def process_like_fanpage(self, percent):
        try:
            print('process like fanpage')
            self.function_like_fanpage(percent)
        except Exception as e:
            print('error in process_like_fanpage')
            print(e)
            self.press_key_in_page_html(Keys.ESCAPE)

    def handling_authentication(self, proxy_authen):
        WebDriverWait(self.web_driver, 20).until(expected_conditions.alert_is_present())
        try:
            alert = self.web_driver.switch_to.alert
            alert.send_keys(proxy_authen['username'] + Keys.TAB + proxy_authen['password'])
            alert.accept()
            self.web_driver.switch_to.default_content()
            return True
        except Exception as e:
            print(e)
            print('Error in handling authentcation')
            return False

    def send_message(self):
        self.get_URL('https://www.facebook.com/lnanhkhoa')
        # message_box = self.driver.find_element_by_css_selector("a[href='https://www.facebook.com/messages/t/100004703621008']")
        message_box = self.driver.find_element_by_css_selector("a[href='/messages/t/lnanhkhoa/']")
        message_box.click()
        time.sleep(5)
        send_box = self.driver.find_element_by_css_selector(".notranslate")
        # time.sleep(10)
        send_box.send_keys("Hi")
        send_box.send_keys(Keys.ENTER)
