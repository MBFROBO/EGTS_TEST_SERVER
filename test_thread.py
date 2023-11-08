from threading import Thread
from collections import deque
import time
# Create a new class that inherits from Thread
class Worker(Thread):
    def __init__(self, inqueue, outqueue, func):
        '''
        A worker that calls func on objects in inqueue and
        pushes the result into outqueue
        runs until inqueue is empty
        '''
        self.inqueue = inqueue
        self.outqueue = outqueue
        self.func = func
        super().__init__()
    # override the run method, this is starte when
    # you call worker.start()
    def run(self):
        while self.inqueue:
            data = self.inqueue.popleft()
            print('start')
            result = self.func(data)
            self.outqueue.append(result)
            print('finished')
def test(x):
    time.sleep(x)
    return 2 * x


if __name__ == '__main__':
    data = 12 * [1, ]
    queue = deque(data)
    result = deque()
    # create 3 workers working on the same input
    workers = [Worker(queue, result, test) for _ in range(3)]
    # start the workers
    for worker in workers:
        worker.start()
    # wait till all workers are finished
    for worker in workers:
        worker.join()
    print(result)