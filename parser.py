import csv
from datetime import datetime

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
                'end': start + length
            })
    return mapping

def convert_dob(dob_raw):
    if len(dob_raw) != 6 or not dob_raw.isdigit():
        return ''
    yy, mm, dd = int(dob_raw[:2]), int(dob_raw[2:4]), int(dob_raw[4:6])
    try:
        year = 2000 + yy if yy < 11 else 1900 + yy
        return datetime(year, mm, dd).strftime('%Y-%m-%d')
    except ValueError:
        return ''

def parse_line(line, mapping):
    record = {}
    for field in mapping:
        value = line[field['start']:field['end']].strip()
        if field['name'].lower() == 'dob':
            value = convert_dob(value)
        record[field['name']] = value
    return record

def parse_text_file(data_path, mapping_path, output_path, bad_data_path):
    mapping = load_mapping(mapping_path)

    with open(data_path, 'r') as infile, \
         open(output_path, 'w', newline='', encoding='utf-8') as goodfile, \
         open(bad_data_path, 'w', newline='', encoding='utf-8') as badfile:

        good_writer = None
        bad_writer = None

        for line_num, line in enumerate(infile, start=1):
            line = line.rstrip('\n').ljust(134)
            parsed = parse_line(line, mapping)

            # Initialize good_writer
            if good_writer is None:
                good_writer = csv.DictWriter(goodfile, fieldnames=parsed.keys())
                good_writer.writeheader()

            good_writer.writerow(parsed)

            # Check for bad DOB and log to bad_data.csv
            if parsed.get('dob', '') == '':
                # Extend the record with raw line and comment
                bad_record = dict(parsed)  # shallow copy
                bad_record['raw_data'] = line.strip()
                bad_record['comment'] = 'Invalid DOB'

                # Initialize bad_writer if needed
                if bad_writer is None:
                    bad_fieldnames = list(parsed.keys()) + ['raw_data', 'comment']
                    bad_writer = csv.DictWriter(badfile, fieldnames=bad_fieldnames)
                    bad_writer.writeheader()

                bad_writer.writerow(bad_record)

# Example usage — adjust filenames if needed
if __name__ == '__main__':
    parse_text_file('./mock_output/mock_names.txt', './input_files_for_parsing/mapping_for_parsing.csv', './parsed_output/parsed_output.csv','./bad_data/bad_data.csv' )

