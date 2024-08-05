import json
import random
import numpy as np
from faker import Faker
from datetime import datetime
from generator.data import real_addresses, form50058

def generate_one_fake_ssn() -> str:
    serial_number = f"{random.choice(range(1, 10000)):04d}"   
    area_number = random.choice(range(900, 1000))   
    group_number = f"{random.choice(range(100)):02d}"
    fake_ssn = f"{area_number}{group_number}{serial_number}"
    return fake_ssn

def generate_members(n_members : int) -> dict:
    fake = Faker('en_US')
    
    members = []

    for i in range(1, n_members + 1):
        sex = random.choice(['M', 'F'])

        if sex == 'M':
            firstname, lastname = fake.first_name_male(), fake.last_name()
        else:
            firstname, lastname = fake.first_name_female(), fake.last_name()
            
        dob = fake.date_of_birth(minimum_age=18)

        member = {
            "memberNumber": f"{i:02}",
            "lastName": lastname,
            "firstName": firstname,
            "middle": "",
            "dob": f"{dob.month:02}{dob.day:02}{dob.year}",
            "age": datetime.now().year - dob.year,
            "sex": sex,
            "relationCode": "H",
            "citizenshipCode": "EC",
            "isDisabled": "Y",
            "raceCode": [
                "1"
            ],
            "ethnicityCode": "2",
            "ssn": generate_one_fake_ssn(),  
            "alienNumber": ""
        }
        members.append(member)
    return members

def generate_address() -> dict:
    """
    Parameters
    ----------
    None

    Returns
    -------
    A dictionary with address information
    """
    addr = random.choice(real_addresses.get('addresses'))
    return {
        'street': addr.get('address1', ''),
        'apartment': addr.get('address2', ''),
        'city': addr.get('city', ''),
        'state': addr.get('state', ''),
        'zip': addr.get('postalCode', ''),
    }

def generate_form(n_entries: int, max_member: int, phaCode: str) -> str:
    forms = []
    
    for _ in range(n_entries):
        js = json.loads(form50058)
        n_members = random.randint(1, max_member + 1)
        js['agency']['phaCode'] = phaCode
        js['household']['members'] = generate_members(n_members)
        js['unitOccupied']['address'] = generate_address()
        forms.append(js)

    output = {
        "form50058": forms
    }

    return json.dumps(output)