import csv
import re
from datetime import datetime
from collections import defaultdict
import os

def parse_text_file(data_path, mapping_path, output_dir='.', bad_data_path='bad_data.csv'):
    os.makedirs(output_dir, exist_ok=True)
    ...


def load_mapping(mapping_path):
    segment_mapping = defaultdict(list)
    with open(mapping_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            field = {
                'name': row['column_name'],
                'start': int(row['starting']),
                'end': int(row['starting']) + int(row['length']),
                'type': row['datatype'].strip().lower(),
                'segment': row['segment_name'].strip()
            }
            segment_mapping[field['segment']].append(field)
    return segment_mapping

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
    return value if re.fullmatch(r'[A-Za-z ]*', value) else ''

def validate_integer(value):
    return value if value.isdigit() else ''

def parse_segment(line, fields):
    record = {}
    bad_reasons = []
    for field in fields:
        raw_value = line[field['start']:field['end']].strip()
        name = field['name']
        dtype = field['type']

        if dtype == 'date' and name.lower() == 'dob':
            value, error = convert_dob(raw_value)
            if error:
                bad_reasons.append(error)
        elif dtype == 'text':
            cleaned = validate_text(raw_value)
            if cleaned != raw_value:
                bad_reasons.append(f"Invalid {name} (non-alpha or symbols)")
            value = cleaned
        elif dtype == 'integer':
            cleaned = validate_integer(raw_value)
            if cleaned != raw_value:
                bad_reasons.append(f"Invalid {name} (non-digit)")
            value = cleaned
        else:
            value = raw_value

        record[name] = value

    return record, bad_reasons

def parse_text_file(data_path, mapping_path, output_dir='.', bad_data_path='bad_data.csv'):
    segment_mapping = load_mapping(mapping_path)
    writers = {}
    fieldnames_map = {}
    files = {}

    with open(data_path, 'r') as infile, \
         open(f"{output_dir}/{bad_data_path}", 'w', newline='', encoding='utf-8') as badfile:

        bad_writer = None

        for line_num, line in enumerate(infile, start=1):
            line = line.rstrip('\n').ljust(134)
            full_bad = False
            all_segment_data = {}

            # Parse each segment
            for segment, fields in segment_mapping.items():
                record, errors = parse_segment(line, fields)
                all_segment_data[segment] = record

                if errors:
                    full_bad = True
                    if bad_writer is None:
                        bad_fields = list(record.keys()) + ['raw_data', 'comment']
                        bad_writer = csv.DictWriter(badfile, fieldnames=bad_fields)
                        bad_writer.writeheader()

                    bad_record = dict(record)
                    bad_record['raw_data'] = line.strip()
                    bad_record['comment'] = "; ".join(errors)
                    bad_writer.writerow(bad_record)

                # Write to appropriate parsed_segment_output.csv
                if segment not in writers:
                    output_file = open(f"{output_dir}/parsed_{segment.lower()}_output.csv", 'w', newline='', encoding='utf-8')
                    fieldnames_map[segment] = list(record.keys())
                    writer = csv.DictWriter(output_file, fieldnames=fieldnames_map[segment])
                    writer.writeheader()
                    writers[segment] = writer
                    files[segment] = output_file

                writers[segment].writerow(record)

    # Close all segment files
    for f in files.values():
        f.close()


# Example usage — adjust filenames if needed
if __name__ == '__main__':
    parse_text_file(
    './mock_output/mock_names.txt',
    './input_files_for_parsing/mapping_for_parsing.csv',
    './parsed_output',          # ✅ A directory to write segmented outputs into
    'bad_data.csv'              # ✅ A filename (will go into output_dir)
)

