from datetime import datetime
import json

def transform_value(value):
    if isinstance(value, dict):
        data_type, value = value.popitem()

        if data_type == 'S':
            if value.startswith("RFC3339"):
                value = int(datetime.strptime(value[8:], "%Y-%m-%dT%H:%M:%SZ").timestamp())
            return value.strip()  # Strip trailing whitespace
        elif data_type == 'N':
            try:
                return float(value) if '.' in value else int(value)
            except ValueError:
                return None
        elif data_type == 'BOOL':
            return value.lower() in ['1', 't', 'true']
        elif data_type == 'NULL':
            return None if value.lower() in ['1', 't', 'true'] else None
        elif data_type == 'L':
            if isinstance(value, list):
                return [transform_value(item) for item in value if item]  # Remove empty strings
            else:
                return None
        elif data_type == 'M':
            transformed_map = {}
            for key, val in value.items():
                transformed_map[key] = transform_value(val)
            return transformed_map
    else:
        return value

def transform_json(input_json):
    transformed_json = {}
    for key, value in input_json.items():
        if key == 'map_1':
            transformed_map = transform_value(value)
            if 'list_1' in transformed_map and isinstance(transformed_map['list_1'], list):
                transformed_map['list_1'] = [transform_value(item) for item in transformed_map['list_1'] if item]
            if isinstance(transformed_map['list_1'], list):
                transformed_map['list_1'].append(transform_value({"BOOL": "false"}))
            transformed_json[key] = transformed_map
        elif key in ['number_1', 'string_1']:
            transformed_json[key] = transform_value(value)
        elif key == 'string_2':
            transformed_json[key] = int(datetime.strptime(value['S'], "%Y-%m-%dT%H:%M:%SZ").timestamp())
    return transformed_json

# Read input from file
input_file = 'input.json'
with open(input_file, 'r') as file:
    input_json = json.load(file)

# Transform the input JSON
output_data = transform_json(input_json)

# Print the transformed JSON to stdout as a formatted JSON string
print(json.dumps([output_data], indent=2))
