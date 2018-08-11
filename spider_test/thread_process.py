# from multiprocessing import Process
import threading

import time


class MyThread(threading.Thread):
    def __init__(self):
        super(MyThread, self).__init__()

    def run(self):
        global n, lock
        time.sleep(1)
        lock.acquire()
        print(n)
        n += 1
        lock.release()#释放锁


if __name__ == '__main__':
    n = 0
    lock = threading.Lock()
    threads = []
    for _ in range(10):
        thread = MyThread()
        threads.append(thread)
    for t in threads:
        t.start()
        t.join()

