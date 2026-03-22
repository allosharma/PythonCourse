import threading
import time

def test():
    print("Thread started with name:", threading.current_thread().name + " and id:", threading.get_ident())
    time.sleep(2)
    print("Thread ended")

def test2(name):
    print(f'Thread start for {name}')
    time.sleep(2)
    print(f"Thread ended for {name}")

if __name__ == "__main__":
    start_time = time.time() # This will store the current time in seconds since the epoch
    t1 = threading.Thread(target = test)
    t2 = threading.Thread(target = test)
    t3 = threading.Thread(target = test)
    t1.start() # This will start the thread t1 and execute the test function in a separate thread
    t2.start() # This will start the thread t2 and execute the test function in a separate thread
    t3.start() # This will start the thread t3 and execute the test function in a separate thread
    t1.join() # This will wait for the thread t1 to finish before moving to the next line of code
    t2.join() # This will wait for the thread t2 to finish before moving to the next line of code
    t3.join() # This will wait for the thread t3 to finish before moving to the next line of code
    print("All threads have finished execution")
    
    names = ['Alok', 'John', 'Alice', 'Bob', 'Charlie', 'David', 'Eve', 'Frank', 'Grace', 'Heidi']
    threads = []
    for name in names:
        thread = threading.Thread(target = test2, args=[name])
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()

    print(f'Total time taken to execute the program: {round(time.time() - start_time, 2)} seconds') # This will print the total time taken to execute the program in seconds with 2 decimal places{time.time() - start_time} seconds')


