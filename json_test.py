import json


def max_len(key, li):
    return f'{key} max len: {max(map(lambda x: len(x[key]), li))}'


# calculating maximum len of DB fields
open("data/versions.json") 
vers = json.load(open("data/versions.json"))

open("data/vulnerabilities.json") 
vuln = json.load(open("data/vulnerabilities.json"))


print("versoins.json")
print(max_len('product', vers))
print(max_len('vendor', vers))
print(max_len('version', vers), "\n")


print("vulnerabilities.json")
print(max_len('product', vuln))
print(max_len('vendor', vuln))
print(max_len('KLA_id', vuln))
print(max_len('description', vuln))
print(max_len('publish_date', vuln))
print(max_len('start_vuln_version', vuln))
print(max_len('fixed_version', vuln))



