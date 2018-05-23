import os
import time
from queue import Queue
from account_instance import AccountInstance


def do_nothing():
    time.sleep(1)
    print( 'now stop')


def do_stuff(q: Queue):
  while getattr(q, 'do_run', True):
    numeric = q.get()
    print('SO THU TU:' + str(numeric))
    instance = AccountInstance(numeric)
    instance.run()
    q.task_done()
