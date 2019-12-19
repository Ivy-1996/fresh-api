import re


def is_legal_phone(phone: str):
    reg = '^1([38][0-9]|4[579]|5[0-3,5-9]|6[6]|7[0135678]|9[89])\d{8}$'
    return re.match(reg, phone)
