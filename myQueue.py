import os
import time
from queue import Queue
from threading import Thread


def do_nothing():
    time.sleep(1)
    print( 'now stop')


def do_stuff(q: Queue):
  while getattr(q, 'do_run', True):
    print(q.get())
    do_nothing()
    # os.system('.\\venv\\Scripts\\python.exe main.py')
    q.task_done()