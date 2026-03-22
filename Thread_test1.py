import time
import threading

class NumberPrinter(threading.Thread):
    def __init__(self, number):
        threading.Thread.__init__(self)
        self.number = number

    def run(self):
        time.sleep(1)
        print(f'Number Printing: {self.number}, Thread Name: {threading.current_thread().name}')

if __name__ == "__main__":
    threads = []
    for i in range(1, 101):
        thread = NumberPrinter(i)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    print("All threads have finished execution")