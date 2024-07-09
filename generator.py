import json
import random
import numpy as np
from faker import Faker
from datetime import datetime
from random_address import real_random_address

form50058 = """
{
    "header": {
        "submissionType": "50058",
        "identificationCode": "19871",
        "vendorSoftwareId": "Yardi",
        "vendorSoftwareVersion": "test",
        "formVersionDate": "2020",
        "vendorDefinedData": "Tenant t0001807"
    },
    "agency": {
        "phaName": "Yardi Housing Authority",
        "phaCode": "DC123",
        "program": "VO",
        "voucherType": "T"
    },
    "action": {
        "actionType": "1",
        "effectiveDate": "07012023",
        "isCorrection": "N",
        "admissionDate": "07012023",
        "reexaminationDate": "02012024",
        "isFssParticipant": "N",
        "specialProgram": "",
        "specialOther1": "",
        "specialOther2": ""
    },
    "household": {
        "members": [
            {
                "memberNumber": "01",
                "lastName": "Welsh",
                "firstName": "Veronica",
                "middle": "",
                "dob": "01141976",
                "age": "47",
                "sex": "F",
                "relationCode": "H",
                "citizenshipCode": "EC",
                "isDisabled": "Y",
                "raceCode": [
                    "1"
                ],
                "ethnicityCode": "2",
                "ssn": "124124124",  
                "alienNumber": ""
            }
        ],
        "totalHousehold": "1",
        "subsidyStatus": "E"
    },
    "background": {
        "waitingListEntryDate": "01202018",
        "zipBeforeAdmission": "11120",
        "isHomelessAtAdmission": "Y",
        "isVeryLowIncomeLimit": "N",	
        "isContinuallyAssisted": "N"
    },
    "unitOccupied": {
        "address": {
            "street": "1248 Nash Street",
            "apartment": "",
            "city": "Santa Barbara",
            "state": "CA",
            "zip": "93105",
            "zipPlus": ""
        }
    },
    "totalTenantPayment": {
            "adjustedMonthlyIncomePercent": "3000"
    }
}
"""

def generate_one_fake_ssn():
    serial_number = f"{random.choice(range(1, 10000)):04d}"   
    area_number = random.choice(range(900, 1000))   
    group_number = f"{random.choice(range(100)):02d}"
    fake_ssn = f"{area_number}{group_number}{serial_number}"
    return fake_ssn

def generate_members(n_members : int) -> object:
    fake = Faker('en_US')
    
    members = []

    for i in range(1, n_members + 1):
        sex = random.choice(['M', 'F'])

        if sex == 'M':
            firstname, lastname = fake.first_name_male(), fake.last_name()
        else:
            firstname, lastname = fake.first_name_female(), fake.last_name()
            
        dob = fake.date_of_birth()

        member = {
            "memberNumber": f"{i:02}",
            "lastName": lastname,
            "firstName": firstname,
            "middle": "",
            "dob": f"{dob.month}{dob.day}{dob.year}",
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

def generate_address():
    addr = real_random_address()
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