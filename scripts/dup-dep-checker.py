"""
resolves conflicts in packages.json
"""
from copy import deepcopy
import json

def print_double_entries():
    """
    Print double entries in packages.json
    """
    with open("packages/packages.json", "r") as f:
        data = json.load(f)

    all_entries = []
    for section in ["dev", "third_party"]:
        all_entries.extend(data.get(section, {}).keys())

    duplicates = set([entry for entry in all_entries if all_entries.count(entry) > 1])

    new_data = deepcopy(data)

    if duplicates:
        print("Duplicate entries found:")
        for entry in duplicates:
            print(f"- {entry}")
            for section in ["third_party", ]:
                if entry in new_data.get(section, {}):
                    del new_data[section][entry]
        with open("packages/packages.json", "w") as f:
            json.dump(new_data, f, indent=4)
            f.write("\n")
            print("Removed duplicates and updated packages.json")
    else:
        print("No duplicate entries found.")

if __name__ == "__main__":
    print_double_entries()