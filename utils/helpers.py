import os
import csv
import random
import string

def get_next_id(filename):
    if not os.path.exists(filename):
        return "1"

    max_id = 0
    with open(filename, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if row and row[0].isdigit():
                max_id = max(max_id, int(row[0]))

    return str(max_id + 1)

def generatePass(length=8):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))
