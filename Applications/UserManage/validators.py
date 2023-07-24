import re
from django.core.exceptions import ValidationError

def apartment_house_num_validator(apartment_num):
    pattern = r'^[0-9][A-Za-z0-9]*$'
    check_status = re.match(pattern, apartment_num)
    if not check_status:
        raise ValidationError("Improper data")
    return True

def street_name_validator(street_name):
    pattern = r'^[A-Za-z\s]*$'
    check_status = re.match(pattern, street_name)
    if not check_status:
        raise ValidationError("Improper data")
    return True


def zip_code_validator(zip_code):
    pattern = r'^\d{2}[-\s]?(?:\d{3})?$'
    check_status = re.match(pattern, zip_code)
    if not check_status:
        raise ValidationError("Improper data")
    return True


