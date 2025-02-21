import gzip
import json
import argparse

def read_compressed_json(file_path):
    with gzip.open(file_path, 'rt', encoding='utf-8') as f:
        data = json.load(f)
    return data

empty_inventory = {'model': {'start': None, 'end': None}, 'hourly': {'start': None, 'end': None}, 'daily': {'start': None, 'end': None}, 'monthly': {'start': None, 'end': None}, 'normals': {'start': None, 'end': None}}
empty_hourly = {'start': None, 'end': None}
def filter_points(points, countries):
    
    print("Before filtering: ", len(points))
    points = [point for point in points if point.get('country') in countries]
    
    print("After filtering countries: ", len(points))
    points = [point for point in points if point.get('inventory', empty_inventory) != empty_inventory]
    
    print("After filtering inventory: ", len(points))
    
    points = [point for point in points if point["inventory"].get('hourly', empty_hourly) != empty_hourly]
    
    print("After filtering no hourly: ", len(points))
    return points
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Filter weather stations by country and relevant data')
    parser.add_argument('file_path', type=str, help='The path to the compressed JSON file')
    args = parser.parse_args()

    file_path = args.file_path
    points = read_compressed_json(file_path)
    selected_countries = ['NL', 'DE', 'DK', 'BE', 'FR', 'GB', 'NO'] # Countries around the North Sea
    filtered_points = filter_points(points, selected_countries)
    output_file_path = file_path.replace('.json.gz', '_filtered.json.gz')
    with gzip.open(output_file_path, 'wt', encoding='utf-8') as f:
        json.dump(filtered_points, f)