import os
import csv
from faker import Faker
from random import randint
from datetime import datetime


# Initialize Faker
fake = Faker()


# Define output directory and file
output_dir = './mock_output/'
output_file = os.path.join(output_dir, 'mock_names.txt')


def generate_random_dob_code():
    # Generate realistic DOB between 1940-2010
    year = randint(1940, 2010)
    month = randint(1, 12)
    
    # Ensure the day is valid for that month/year
    if month == 2:
        day = randint(1, 29 if year % 4 == 0 else 28)
    elif month in [4, 6, 9, 11]:
        day = randint(1, 30)
    else:
        day = randint(1, 31)
    
    # Format as YYMMDD (2-digit year)
    return f"{year % 100:02d}{month:02d}{day:02d}"

# Create the directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)


# Number of mock records
num_records = 50000
written = 0


with open(output_file, 'w', encoding='utf-8') as file:
    while written < num_records:
        first_name = fake.first_name()
        last_name = fake.last_name()
        if len(first_name) > 20 or len(last_name) > 20:
            continue  # Skip long names

        dob_code = generate_random_dob_code()
        address = fake.street_address()[:40]
        city = fake.city()[:28]
        state = fake.state_abbr()
        zip_code = fake.zipcode()[:5]

        line = (
            f"{first_name:<20}"
            f"{last_name:<20}"
            f"{dob_code}"
            f"{address:<40}"
            f"{city:<28}"
            f"{state:<2}"
            f"{zip_code:<5}"
        )
        file.write(line + '\n')
        written += 1
print(f"Created {num_records} records at: {output_file}")

#mapping
#first column segment name such as bio, entitlements, dates, payments, suspense
#segment name  bio  #column name such as first_name, last_name, dob
#starting point ending point start at 0 end at 
