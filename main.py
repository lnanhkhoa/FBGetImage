#!/usr/bin/python
import logging
import os
import time
import apps
from config import DATABASE_CONFIG

# Current path directory
cur_path = os.path.dirname(__file__)
# Apps
# display = Display(visible=0, size=(800, 600))
# display.start()
tinydbInfoAcc = apps.TinyDBInfoAcc()
functionsWebDriver = apps.FunctionsWebDriver('firefox', tinydbInfoAcc)

# Information Users Facebook
user = DATABASE_CONFIG['username']
password = DATABASE_CONFIG['password']
accountFacebook = apps.AccountsFacebook(user, password)

# Scripts
text_search = DATABASE_CONFIG['text_search']
type_of_run_script = DATABASE_CONFIG['type_of_run_script']


def preprocessor():
    functionsWebDriver.get_url('https://www.facebook.com/')
    functionsWebDriver.login(accountFacebook)
    searchPage = functionsWebDriver.get_url(
        'https://www.facebook.com/search/str/' + text_search + '/stories-keyword/today/date/stories/intersect')
    # functionsWebDriver.load_all_post_search()
    # functionsWebDriver.process_like_fanpage(0.5)
    # functionsWebDriver.click_see_more()

def databasesShow():
    tinydbInfoAcc.show_all()


def main():
    print("==========================================")
    listName = functionsWebDriver.get_list_name_container()
    len1ist = len(listName)
    print('So container: ' + str(len1ist))
    for name in listName:
        print('')
        print('!!!===!!!' + name + '!!!===!!!')
        print('')
        functionsWebDriver.process_in_container(name)

def finish_process():
    pass
    # functionsWebDriver.logout()
    # functionsWebDriver.quit()

if __name__ == '__main__':
    start = time.time()
    preprocessor()
    main()
    finish_process()
    end = time.time()
    print("Script xai het :" + str(end - start))
    # display.stop()
