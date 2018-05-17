#!/usr/bin/python
import logging
import os
import time
from pyvirtualdisplay import Display
import apps
from config import DATABASE_CONFIG

# Current path directory
cur_path = os.path.dirname(__file__)

# Logging
# logger = logging.getLogger('myapp')
# hdlr = logging.FileHandler(os.path.join(cur_path, 'log/myapp.log'))
# formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
# hdlr.setFormatter(formatter)
# logger.addHandler(hdlr)
# logger.setLevel(logging.WARNING)

# Apps
display = Display(visible=0, size=(1024, 768))
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
    functionsWebDriver.load_all_post_search()
    functionsWebDriver.process_like_fanpage(0.5)
    functionsWebDriver.click_see_more()
    print('load All Done')


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


def test():
    pass


if __name__ == '__main__':
    start = time.time()
    preprocessor()
    main()
    functionsWebDriver.quit()
    end = time.time()
    print("Script xai het :" + str(end - start))
    functionsWebDriver.quit()
    # display.stop()
