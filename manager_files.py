import os

cur_path = os.path.dirname(__file__)
files_directory = os.path.join(cur_path, 'files')
list_accounts_dir = os.path.join(files_directory, 'accs.txt')
list_proxies_dir = os.path.join(files_directory, 'proxy.txt')

with open(list_accounts_dir, 'r') as handle:
    list_acc_with_pass = handle.readlines()
with open(list_proxies_dir, 'r') as handle1:
    list_proxy = handle1.readlines()


def get_username_with_number(number):
    user = list_acc_with_pass[number * 2][:-1]
    passwd = list_acc_with_pass[number * 2 + 1][:-1]
    return user, passwd


def number_of_accounts():
    return list_acc_with_pass.__len__() / 2


def number_of_proxy():
    return list_proxy.__len__()


def get_proxy(number):
    index_proxy = int(number / 50)
    return list_proxy[index_proxy][:-1]
