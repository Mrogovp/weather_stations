import gzip
import json
import argparse

def read_compressed_json(file_path):
    with gzip.open(file_path, 'rt', encoding='utf-8') as f:
        data = json.load(f)
    return data

def filter_points(points, countries):
    points = [point for point in points if point.get('country') in countries]
    points = [point for point in points if not all(value is None for value in point.get('inventory', {}).values())]
    return points
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process a compressed JSON file.')
    parser.add_argument('file_path', type=str, help='The path to the compressed JSON file')
    args = parser.parse_args()

    file_path = args.file_path
    points = read_compressed_json(file_path)
    selected_countries = ['NL', 'DE', 'DK', 'BE', 'FR', 'GB']
    filtered_points = filter_points(points, selected_countries)
    output_file_path = file_path.replace('.json.gz', '_filtered.json.gz')
    with gzip.open(output_file_path, 'wt', encoding='utf-8') as f:
        json.dump(filtered_points, f)