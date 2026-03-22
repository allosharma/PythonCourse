from multiprocessing import Process
import time

def heavy_task(name):
    print(f"Process {name} started")
    
    # Simulate CPU heavy work
    total = 0
    for i in range(10_000_000_0):
        total += i

    print(f"Process {name} finished")

if __name__ == "__main__":
    # Sequential execution
    start_time_Sequntial = time.time()
    heavy_task('Test1')
    heavy_task('Test2')
    print(f"Sequential process took {time.time() - start_time_Sequntial:.2f} seconds)")

    # Parallel execution using multiprocessing
    p1 = Process(target=heavy_task, args=("Test1",))
    p2 = Process(target=heavy_task, args=("Test2",))

    start_time_multiprocessing = time.time()

    p1.start()  # Start process A
    p2.start()  # Start process B

    p1.join()   # Wait for process A
    p2.join()   # Wait for process B

    end = time.time()
    print(f"Multiprocessing took {end - start_time_multiprocessing:.2f} seconds")