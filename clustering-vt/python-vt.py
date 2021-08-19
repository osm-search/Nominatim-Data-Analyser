import argparse
import mapbox_vector_tile
import sys
import json
from pathlib import Path
import os
parser = argparse.ArgumentParser(prog='python-vt')

# parser.add_argument('--execute', action='store_true', help='Executes all the QA rules')
# parser.add_argument('--filter', metavar='<QA rules names>', nargs='+', help='Filters some QA rules so they are not executed.')
parser.add_argument('--output', metavar='<output>', action='store', type=str, help='output file')

args = parser.parse_args()

if not sys.stdin.isatty():
    input = sys.stdin.read()

# if args.output:
decoded = json.loads(input)
to_encode = list()
print(decoded)

for feature in decoded:
    new_dict = dict()
    for k, v in feature.items():
        if k == 'geometry':
            new_dict[k] = f'Point({v[0][0]} {v[0][1]})'
        elif k == 'tags':
            new_dict['properties'] = v
        else:
            new_dict[k] = v
    to_encode.append(new_dict)

print(to_encode)
encoded = mapbox_vector_tile.encode([{
    'name': 'clusterLayer',
    'features': to_encode
}], extents=256, y_coord_down=True)

Path(os.path.dirname(args.output)).mkdir(parents=True, exist_ok=True)

# sys.stdout.buffer.write(encoded)
with open(args.output, 'wb') as file:
    file.write(encoded)