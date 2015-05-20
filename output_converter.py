# convert [78705, {"count": 28, "is_happy": 23, "ratio": 0.8214285714285714}] to CSV
import json
import csv
import sys


f = open(sys.argv[1])
lines = f.read().splitlines()
fieldnames = ['zipcode', 'ratio', 'count']

csv_file = open(sys.argv[2], 'w')
writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
writer.writerow({name: name for name in fieldnames})
for line in lines:
    data = json.loads(line)
    zipcode = data[0]
    writer.writerow({
        'zipcode': zipcode,
        'ratio': data[1]['ratio'],
        'count': data[1]['count']
    })

f.close()
csv_file.close()
