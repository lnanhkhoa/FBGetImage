#!/usr/bin/python
import time
import apps
from config import DATABASE_CONFIG
from manager_files import *

# Current path directory
cur_path = os.path.dirname(__file__)

# Scripts
text_search = DATABASE_CONFIG['text_search']
type_of_run_script = DATABASE_CONFIG['type_of_run_script']


class AccountInstance:
    def __init__(self, numeric):
        self.numeric = numeric
        # Information Users Facebook
        user, password = get_username_with_number(numeric)
        self.accountFacebook = apps.AccountsFacebook(user, password)
        # Apps
        self.tinydb_info_acc = apps.TinyDBInfoAcc()
        self.functionsWebDriver = apps.FunctionsWebDriver('firefox', self.tinydb_info_acc, numeric)

    def preprocessor(self):
        self.functionsWebDriver.get_url('https://www.facebook.com/')
        self.functionsWebDriver.login(self.accountFacebook)
        self.functionsWebDriver.get_url(
            'https://www.facebook.com/search/str/' + text_search + '/stories-keyword/today/date/stories/intersect')
        is_checkpoint = self.functionsWebDriver.check_checkpoint()
        if is_checkpoint == False:
            self.functionsWebDriver.load_all_post_search()
            self.functionsWebDriver.process_like_fanpage(0.5)
        return is_checkpoint
        # functionsWebDriver.click_see_more()

    def main_process(self):
        print("==========================================")
        list_name = self.functionsWebDriver.get_list_name_container()
        len1ist = len(list_name)
        print('So container: ' + str(len1ist))
        for name in list_name:
            print('')
            print('!!!===!!!' + name + '!!!===!!!')
            print('')
            self.functionsWebDriver.process_in_container(name)

    def finish_process(self):
        # os.system('python apps\mail.py')
        self.functionsWebDriver.logout()

    def run(self):
        start = time.time()
        authen_proxy = self.functionsWebDriver.is_authen()
        if authen_proxy == True:
            is_checkpoint = self.preprocessor()
            if is_checkpoint == False:
                self.main_process()
            else:
                print("Acc " + str(self.numeric) + " da bi checkpoint")
                self.tinydb_info_acc.insert_acc(self.accountFacebook.username)
            self.finish_process()
        else:
            print('not authen proxy')
        self.functionsWebDriver.quit()
        end = time.time()
        print("Thoi gian run account " + str(self.numeric) + ": " + str(end - start))
