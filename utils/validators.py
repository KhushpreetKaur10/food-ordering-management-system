import re

def is_valid_email(email):
    return re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email)

def is_valid_phone(phone):
    return phone.isdigit() and len(phone) == 10