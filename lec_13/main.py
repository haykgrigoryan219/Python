import time
import random
import string
from threading import Thread
from multiprocessing import Process, Lock, Manager

# Function to generate a large text file with random words
def generate_large_file(filename, num_words=1000000):
    with open(filename, 'w') as file:
        for _ in range(num_words):
            word = ''.join(random.choices(string.ascii_lowercase, k=random.randint(3, 10)))
            file.write(word + " ")
            if random.random() < 0.1:
                file.write("\n")

# Sequential word count function
def count_words_sequential(filename):
    word_count = {}
    with open(filename, 'r') as file:
        for line in file:
            for word in line.split():
                word_count[word] = word_count.get(word, 0) + 1
    return word_count

# Function to count words in chunks for multithreading
def count_words_threaded_chunk(filename, start, end, word_count, lock):
  local_word_count = {}
  with open(filename, 'r') as file:
      file.seek(start)
      while file.tell() < end:
          line = file.readline()
          for word in line.split():
              local_word_count[word] = local_word_count.get(word, 0) + 1
  # Lock to safely update the word count
  with lock:
      for word, count in local_word_count.items():
          word_count[word] = word_count.get(word, 0) + count

# Multithreading word count function
def count_words_multithreaded(filename):
    word_count = {}
    lock = Lock()
    threads = []
    
    with open(filename, 'r') as file:
        file.seek(0, 2)
        file_size = file.tell()
        file.seek(0)
        num_threads = 4  # Number of threads (you can increase this)
        chunk_size = file_size // num_threads
        start_pos = 0
        
        for i in range(num_threads):
            end_pos = start_pos + chunk_size if (i < num_threads - 1) else file_size
            thread = Thread(target=count_words_threaded_chunk, args=(filename, start_pos, end_pos, word_count, lock))
            threads.append(thread)
            thread.start()
            start_pos = end_pos
        
        for thread in threads:
            thread.join()
    
    return word_count

# Function to count words in chunks for multiprocessing
def count_words_multiprocessing_chunk(filename, start, end, word_count_dict, index, lock):
    local_word_count = {}
    with open(filename, 'r') as file:
        file.seek(start)
        while file.tell() < end:
            line = file.readline()
            for word in line.split():
                local_word_count[word] = local_word_count.get(word, 0) + 1
    # Lock to safely update the word count
    with lock:
        word_count_dict[index] = local_word_count

# Multiprocessing word count function
def count_words_multiprocessing(filename):
  
  with Manager() as manager:
    word_count_dict = manager.dict()
    lock = Lock()
    processes = []
    
    with open(filename, 'r') as file:
        file.seek(0, 2)
        file_size = file.tell()
        file.seek(0)
        num_processes = 4  # Number of processes (you can increase this)
        chunk_size = file_size // num_processes
        start_pos = 0
        
        for i in range(num_processes):
            end_pos = start_pos + chunk_size if i < num_processes - 1 else file_size
            process = Process(target=count_words_multiprocessing_chunk, args=(filename, start_pos, end_pos, word_count_dict, i, lock))
            processes.append(process)
            process.start()
            start_pos = end_pos
        
        for process in processes:
            process.join()
    
    # Merge results from all processes
    word_count = {}
    for local_word_count in word_count_dict.values():
        for word, count in local_word_count.items():
            word_count[word] = word_count.get(word, 0) + count
    
    return word_count

# Timing function for different approaches
def time_function(func, *args):
    start_time = time.time()
    result = func(*args)
    end_time = time.time()
    return result, end_time - start_time

if __name__ == '__main__':
    filename = "large_text_file.txt"
    generate_large_file(filename)  # Generate the file

    # Test sequential approach
    print("Testing Sequential Approach...")
    word_count_sequential, time_sequential = time_function(count_words_sequential, filename)
    print(f"Sequential Time: {time_sequential:.4f} seconds. count = {len(word_count_sequential)}")

    # Test multithreading approach
    print("\nTesting Multithreading Approach...")
    word_count_threaded, time_threaded = time_function(count_words_multithreaded, filename)
    print(f"Multithreading Time: {time_threaded:.4f} seconds. count = {len(word_count_threaded)}")

    # Test multiprocessing approach
    print("\nTesting Multiprocessing Approach...")
    word_count_multiprocessing, time_multiprocessing = time_function(count_words_multiprocessing, filename)
    print(f"Multiprocessing Time: {time_multiprocessing:.4f} seconds. count = {len(word_count_multiprocessing)}")

    # Speedup calculations
    speedup_threaded = time_sequential / time_threaded
    speedup_multiprocessing = time_sequential / time_multiprocessing

    print(f"\nSpeedup (Multithreading vs Sequential): {speedup_threaded:.2f}")
    print(f"Speedup (Multiprocessing vs Sequential): {speedup_multiprocessing:.2f}")
