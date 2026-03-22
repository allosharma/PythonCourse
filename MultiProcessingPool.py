from multiprocessing import Pool
import time
import os

def calculate_cube(num):
    print(f"Calculating cube of {num}")
    time.sleep(1)  # Simulate a time-consuming task
    return num ** 3


if __name__ == "__main__":
    numbers = [10, 20, 30, 40, 50]
    # Sequential execution
    start_time_sequential = time.time()
    sequential_results = [calculate_cube(num) for num in numbers]
    end_time_sequential = time.time()

    print(f"Sequential results: {sequential_results}")
    print(f"Sequential execution took {end_time_sequential - start_time_sequential:.2f} seconds.")

    # Create a multiprocessing pool with 4 processes
    # with Pool(processes = os.cpu_count()) as pool: # Use all available CPU cores
    with Pool(processes=4) as pool:
        start_time = time.time()
        # Map the calculate_cube function to the numbers list
        results = pool.map(calculate_cube, numbers)
        end_time = time.time()

    print(f"Results: {results}")
    print(f"Multiprocessing pool took {end_time - start_time:.2f} seconds.")