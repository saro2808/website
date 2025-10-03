import json

def update(dct, key):
    if key in dct.keys():
        dct[key] += 1
    else:
        dct[key] = 1

with open('asn_ip.json', 'r') as f:
    data = json.load(f)

asn_counts = {}
for ip, value in data.items():
    update(asn_counts, value['asn'])

asn_counts = dict(sorted(asn_counts.items(), key=lambda x: x[0]))

with open('asn_counts.json', 'w+') as f:
    json.dump(asn_counts, f, indent=4)

print('Done. Saved to asn_counts.json')
