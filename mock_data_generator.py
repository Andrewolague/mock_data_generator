import os
import csv
from faker import Faker

# Initialize Faker
fake = Faker()


# Define output directory and file
output_dir = './mock_output/'
output_file = os.path.join(output_dir, 'mock_names.csv')


# Create the directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)


# Number of mock records
num_records = 50000


# Write mock data to CSV
with open(output_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['first_name', 'last_name'])  # Header
    for _ in range(num_records):
        first_name = fake.first_name()
        last_name = fake.last_name()
        writer.writerow([first_name, last_name])


print(f"Created {num_records} records at: {output_file}")
