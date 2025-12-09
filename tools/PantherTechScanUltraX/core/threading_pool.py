# core/threading_pool.py

from concurrent.futures import ThreadPoolExecutor

def run_threads(function, items, threads=100):
    results = []
    with ThreadPoolExecutor(max_workers=threads) as executor:
        for result in executor.map(function, items):
            results.append(result)
    return results
