import csv
from datetime import datetime

# Step 1: Load the mapping
def load_mapping(mapping_path):
    with open(mapping_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        mapping = []
        for row in reader:
            mapping.append({
                'name': row['column_name'],
                'start': int(row['starting']),
                'end': int(row['ending']),
                'type': row['datatype'].split()[-1]  # supports "20 text", "46 date", etc.
            })
        return mapping

# Step 2: Parse a line using the mapping
def parse_line(line, mapping):
    record = {}
    for field in mapping:
        raw_value = line[field['start']:field['end']].strip()
        if field['type'] == 'integer':
            value = int(raw_value) if raw_value.isdigit() else None
        elif field['type'] == 'date':
            try:
                value = datetime.strptime(raw_value, "%m%d%y").date()
            except ValueError:
                value = None
        else:
            value = raw_value
        record[field['name']] = value
    return record

# Step 3: Parse entire file and export to CSV
def parse_text_file(data_path, mapping_path, output_path):
    mapping = load_mapping(mapping_path)
    with open(data_path, 'r') as infile, open(output_path, 'w', newline='') as outfile:
        writer = None
        for line in infile:
            record = parse_line(line, mapping)
            if writer is None:
                writer = csv.DictWriter(outfile, fieldnames=record.keys())
                writer.writeheader()
            writer.writerow(record)

# Example usage — adjust filenames if needed
if __name__ == '__main__':
    parse_text_file('./mock_output/mock_names.txt', './input_files_for_parsing/mapping_for_parsing.csv', './parsed_output/parsed_output.csv')
