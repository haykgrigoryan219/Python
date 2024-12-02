import random
import time

def measure_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()  # Capture start time
        result = func(*args, **kwargs)
        end_time = time.time()  # Capture end time
        print(f"Function {func.__name__} executed in {end_time - start_time:.6f} seconds.")
        return result
    return wrapper

# Step 1: Create a file with 100 lines, each containing 20 random numbers
@measure_time
def create_file(file_name):
    with open(file_name, 'w') as file:
        for _ in range(100):
            line = ' '.join(str(random.randint(0, 100)) for _ in range(20))  # 20 random numbers per line
            file.write(line + '\n')

# Step 2: Read the file and process each line using map and filter
@measure_time
def process_file(file_name):
    with open(file_name, 'r') as file:
        # Use map to convert each line into a list of integers
        lines = file.readlines()
        processed_lines = []
        
        for line in lines:
            numbers = list(map(int, line.split()))  # Convert each number in the line to an integer
            filtered_numbers = list(filter(lambda x: x > 40, numbers))  # Filter numbers > 40
            processed_lines.append(filtered_numbers)
        
    return processed_lines

# Step 3: Write filtered data back to the file
@measure_time
def write_filtered_data(file_name, processed_lines):
    with open(file_name, 'w') as file:
        for line in processed_lines:
            file.write(' '.join(str(num) for num in line) + '\n')

# Step 4: Generator function to read the file
def read_file_as_generator(file_name):
    with open(file_name, 'r') as file:
        for line in file:
            yield list(map(int, line.split()))  # Yield each line as a list of integers

@measure_time
def print_file(file_name):
  for line in read_file_as_generator(file_name):
    print(line)

    
file_name = "random_numbers.txt"

# Create the file with random numbers
create_file(file_name)
    
# Process the file (convert and filter numbers)
processed_lines = process_file(file_name)
    
# Write the filtered data back to the file
write_filtered_data(file_name, processed_lines)
    
# Read the file as a generator
print_file(file_name)
