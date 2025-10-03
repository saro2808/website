import json
import bisect
from ipwhois import IPWhois

def find(ip_dict, ip):
    ips = list(ip_dict.keys())

    idx = bisect.bisect_left(ips, ip)

    if idx < len(ip_dict) and ips[idx] == ip:
        return idx
    return -1

# Load your JSON file
with open("ips.json") as f:
    data = json.load(f)['ip_dict']

results = {}
try:
    with open('asn_ip.json') as f:
        results = json.load(f)
except Exception:
    print('Creating new asn_ip.json')

for ip in data.keys():

    if find(results, ip) != -1:
        continue
    
    print(f'Doing {ip}')
    
    try:
        obj = IPWhois(ip)
        res = obj.lookup_rdap()
        results[ip] = {
            "asn": res.get("asn"),
            "asn_description": res.get("asn_description"),
            "asn_country_code": res.get("asn_country_code")
        }
    except Exception as e:
        results[ip] = {"error": str(e)}

results = dict(sorted(results.items(), key=lambda x: x[0]))

# Save results
with open("asn_ip.json", "w") as f:
    json.dump(results, f, indent=4)

print("Done! Results saved in asn_ip.json")

