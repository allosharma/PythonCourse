import asyncio
import threading
import time

def sync_function():
    print("Starting synchronous function...")
    time.sleep(2)  # Simulate a time-consuming task
    print("Synchronous function completed.")

async def async_function():
    print("Starting asynchronous function...")
    await asyncio.sleep(2)  # Simulate a time-consuming task
    print("Asynchronous function completed.")


def threading_function():
    print('Starting threading test...')
    time.sleep(2)
    print('Threading test completed.')

if __name__ == "__main__":
    # Run the synchronous function
    start_time_sync = time.time()
    sync_function()
    sync_function()
    print(f"Synchronous function took {time.time() - start_time_sync:.2f} seconds.")

    # Run the asynchronous function
    start_time_async = time.time()
    async def main_async():
        await asyncio.gather(async_function(), async_function())
    asyncio.run(main_async())
    print(f"Asynchronous function took {time.time() - start_time_async:.2f} seconds.")

    # Run the threading test
    start_time_threading = time.time()
    t1 = threading.Thread(target=threading_function)
    t2 = threading.Thread(target=threading_function)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    print(f"Threading test took {time.time() - start_time_threading:.2f} seconds.")
