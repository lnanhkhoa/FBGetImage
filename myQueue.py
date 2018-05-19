import os
from queue import Queue
from threading import Thread

def do_stuff(q: Queue):
  while True:
    print(q.get())
    os.system('.\\venv\\Scripts\\python.exe main.py')
    q.task_done()