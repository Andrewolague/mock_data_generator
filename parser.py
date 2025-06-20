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
    """
    Converts 'YYMMDD' to 'YYYY-MM-DD'.
    Years < 11 are treated as 2000s; otherwise, 1900s.
    """
    if len(dob_raw) != 6 or not dob_raw.isdigit():
        return dob_raw  # Return raw if not valid format

    yy = int(dob_raw[:2])
    mm = int(dob_raw[2:4])
    dd = int(dob_raw[4:6])

    try:
        year = 2000 + yy if yy < 11 else 1900 + yy
        dob = datetime(year, mm, dd)
        return dob.strftime('%Y-%m-%d')
    except ValueError:
        return dob_raw  # Return raw if date is invalid


def parse_line(line, mapping):
    record = {}
    for field in mapping:
        value = line[field['start']:field['end']].strip()
        if field['name'].lower() == 'dob':
            value = convert_dob(value)
        record[field['name']] = value
    return record

def parse_text_file(data_path, mapping_path, output_path):
    mapping = load_mapping(mapping_path)
    with open(data_path, 'r') as infile, open(output_path, 'w', newline='', encoding='utf-8') as outfile:
        writer = None
        for line in infile:
            line = line.rstrip('\n').ljust(134)
            record = parse_line(line, mapping)
            if writer is None:
                writer = csv.DictWriter(outfile, fieldnames=record.keys())
                writer.writeheader()
            writer.writerow(record)

# Example usage — adjust filenames if needed
if __name__ == '__main__':
    parse_text_file('./mock_output/mock_names.txt', './input_files_for_parsing/mapping_for_parsing.csv', './parsed_output/parsed_output.csv')

