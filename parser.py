import csv
from datetime import datetime
import re

def load_mapping(mapping_path):
    mapping = []
    with open(mapping_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            start = int(row['starting'])
            length = int(row['length'])
            mapping.append({
                'name': row['column_name'],
                'start': start,
                'end': start + length,
                'type': row['datatype'].strip().lower()  # e.g., 'text', 'date', 'integer'
            })
    return mapping

def convert_dob(dob_raw):
    if len(dob_raw) != 6 or not dob_raw.isdigit():
        return '', 'Invalid DOB'
    yy, mm, dd = int(dob_raw[:2]), int(dob_raw[2:4]), int(dob_raw[4:6])
    try:
        year = 2000 + yy if yy < 11 else 1900 + yy
        return datetime(year, mm, dd).strftime('%Y-%m-%d'), ''
    except ValueError:
        return '', 'Invalid DOB'



def validate_text(value):
    """
    Allows only alphabetic characters and spaces.
    Returns the value if valid, otherwise returns ''.
    """
    if re.fullmatch(r'[A-Za-z ]*', value):
        return value
    return ''


def parse_line(line, mapping):
    record = {}
    bad_reasons = []

    for field in mapping:
        raw_value = line[field['start']:field['end']].strip()
        dtype = field['type']
        fname = field['name']

        # Validate based on type
        if dtype == 'date' and fname.lower() == 'dob':
            value, error = convert_dob(raw_value)
            if error:
                bad_reasons.append(error)
        elif dtype == 'text':
            cleaned = validate_text(raw_value)
            if cleaned != raw_value:
                    bad_reasons.append(f"Invalid {fname} (non-alpha or symbols)")
            value = cleaned
        else:
            value = raw_value  # Future types can go here

        record[fname] = value

    return record, bad_reasons

def parse_text_file(data_path, mapping_path, output_path, bad_data_path):
    mapping = load_mapping(mapping_path)

    with open(data_path, 'r') as infile, \
         open(output_path, 'w', newline='', encoding='utf-8') as goodfile, \
         open(bad_data_path, 'w', newline='', encoding='utf-8') as badfile:

        good_writer = None
        bad_writer = None

        for line_num, line in enumerate(infile, start=1):
            line = line.rstrip('\n').ljust(134)
            record, errors = parse_line(line, mapping)

            # Initialize writers
            if good_writer is None:
                good_writer = csv.DictWriter(goodfile, fieldnames=record.keys())
                good_writer.writeheader()

            if bad_writer is None:
                bad_fields = list(record.keys()) + ['raw_data', 'comment']
                bad_writer = csv.DictWriter(badfile, fieldnames=bad_fields)
                bad_writer.writeheader()

            # Always write to main output
            good_writer.writerow(record)

            # Log bad data if any error detected
            if errors:
                bad_record = dict(record)
                bad_record['raw_data'] = line.strip()
                bad_record['comment'] = "; ".join(errors)
                bad_writer.writerow(bad_record)

# Example usage — adjust filenames if needed
if __name__ == '__main__':
    parse_text_file('./mock_output/mock_names.txt', './input_files_for_parsing/mapping_for_parsing.csv', './parsed_output/parsed_output.csv','./bad_data/bad_data.csv' )

