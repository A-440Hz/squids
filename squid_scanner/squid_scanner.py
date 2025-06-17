#!/usr/bin/env python3
"""
squid_scanner.py

Description: scans all media files in the parent directory and outputs a json file in the following format:
Author: Haotian
Date: 2025-06-02
"""

import json
import os

CD = os.path.dirname(__file__)
MEDIA_DIR = os.path.join(CD, "../")
JSON_OUTPUT = os.path.join(CD, 'collectables.json')
INVALIDS_TXT = os.path.join(CD, 'invalid.txt')

VALID_FILETYPES = (".jpg", ".png", ".mp4", ".webm")
IMAGE_FILETYPES = (".jpg", ".png")
VALID_STATUS = ("S", "A", "B", "C")
SEPARATOR = '-'

def sift_files():
    valid_objs = []
    invalid_files = []
    print(CD)
    for file in os.listdir(MEDIA_DIR):
        fname, ext = os.path.splitext(file)
        if not ext in VALID_FILETYPES:
            invalid_files.append(file + " -- invalid filetype\n")
            continue
        prefix = fname.split(SEPARATOR)
        if len(prefix) != 3:
            invalid_files.append(file + " -- missing field(s)\n")
            continue
        badfields = []
        if not prefix[0].isdigit():
            badfields.append("invalid ID")
        if prefix[2] not in VALID_STATUS:
            badfields.append("invalid status")
        if len(badfields) > 0:
            invalid_files.append(file + ' -- ' + ', '.join(badfields) + '\n')
            continue
        valid_objs.append({
            "ID": int(prefix[0]),
            "Name": prefix[1],
            "Value": prefix[2],
            "Type": "image" if ext in IMAGE_FILETYPES else "media",
            "Filename": file,

        })
    return valid_objs, invalid_files

def main():   
    valids, invalids = sift_files()
    print("\nvalids:\n")
    [print(v) for v in valids]
    print("\n\ninvalids:\n")
    [print(v) for v in invalids]
    with open(JSON_OUTPUT, 'w') as o:
        json.dump(valids, o, indent=4)
    with open(INVALIDS_TXT, 'w') as o:
        o.writelines(invalids)

if __name__ == "__main__":
    main()
