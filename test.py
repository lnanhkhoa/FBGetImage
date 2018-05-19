import configparser
config = configparser.ConfigParser()
config['DEFAULT'] = {}
config['DATABASE_CONFIG'] = {
    'text_search' : "need this shirt",
    'path_image' : 'image',
    'tree_path' : '2',
    'username' : 'uhjcck89333@piupiu.tk',
    'password' : 'qeqeqe123',
    'enable_change_proxy' : True,
    'proxy_host' : '146.71.87.251',
    'proxy_port' : '65233',
    'proxy_username' : 'vannhan24',
    'proxy_password' : 'B8a2ZgA',
    'type_of_run_script' : 1  # 0 is default (testing, not release), 1 is faster run script
}
with open('config.ini', 'w') as configfile:
  config.write(configfile)