import threading

from datetime import datetime


class MyThread(threading.Thread):
    def __init__(self, func):
        super(MyThread, self).__init__()
        self.func = func

    def run(self):
        self.result = self.func

    def get_result(self):
        return self.result


def add_counter(a, b):
    n = 0
    for _ in range(a, b):
        n += 1
    return n


if __name__ == '__main__':
    conter = 0
    lock = threading.Lock()
    t1 = MyThread(add_counter(0, 10000))
    t2 = MyThread(add_counter(10000, 20000))
    t3 = MyThread(add_counter(20000, 30000))
    start_time = datetime.now()
    t1.start()
    t2.start()
    t3.start()
    t1.join()
    t2.join()
    t3.join()
    end_time = datetime.now()
    print(end_time - start_time)
    # start_time = datetime.now()
    # add_counter(0, 30000)
    # end_time = datetime.now()
    # print(end_time - start_time)





