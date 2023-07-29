import re
from django.core.exceptions import ValidationError

def registration_num_validator(apartment_num):
    pattern = r'^[A-Z]{2,3}\s\d{5}$'
    check_status = re.search(pattern, apartment_num)
    print(check_status)
    if not check_status:
        raise ValidationError("Improper data passed to register number")
