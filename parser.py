import csv

# Step 1: Load mapping
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

# Step 2: Parse a single line using mapping
def parse_line(line, mapping):
    record = {}
    for field in mapping:
        value = line[field['start']:field['end']].strip()
        record[field['name']] = value
    return record

# Step 3: Parse entire file and write to CSV
def parse_text_file(data_path, mapping_path, output_path):
    mapping = load_mapping(mapping_path)
    with open(data_path, 'r') as infile, open(output_path, 'w', newline='', encoding='utf-8') as outfile:
        writer = None
        for line in infile:
            line = line.rstrip('\n').ljust(134)  # Ensure full line width
            record = parse_line(line, mapping)
            if writer is None:
                writer = csv.DictWriter(outfile, fieldnames=record.keys())
                writer.writeheader()
            writer.writerow(record)

# Example usage — adjust filenames if needed
if __name__ == '__main__':
    parse_text_file('./mock_output/mock_names.txt', './input_files_for_parsing/mapping_for_parsing.csv', './parsed_output/parsed_output.csv')

