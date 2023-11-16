from multiprocessing import Pool, cpu_count
import time

def factorize_number(number):
    factors = []
    for i in range(1, number + 1):
        if number % i == 0:
            factors.append(i)
    return factors

def factorize_parallel(numbers):
    with Pool(cpu_count()) as pool:
        result = pool.map(factorize_number, numbers)
    return result

def factorize(*numbers):
    return factorize_parallel(numbers)

# Test the function
if __name__ == "__main__":
    start_time_sync = time.time()
    a_sync, b_sync, c_sync, d_sync = factorize(128, 255, 99999, 10651060)
    end_time_sync = time.time()
    print(f"Synchronous execution time: {end_time_sync - start_time_sync:.4f} seconds")

    start_time_parallel = time.time()
    a_parallel, b_parallel, c_parallel, d_parallel = factorize_parallel([128, 255, 99999, 10651060])
    end_time_parallel = time.time()
    print(f"Parallel execution time: {end_time_parallel - start_time_parallel:.4f} seconds")

    # Check correctness of results
    assert a_sync == a_parallel
    assert b_sync == b_parallel
    assert c_sync == c_parallel
    assert d_sync == d_parallel
