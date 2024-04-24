#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 22:41:26 2024

@author: nsuter
"""

""" taken from https://eepublicdownloads.entsoe.eu/clean-documents/EDI/Library/EIC_Reference_Manual_Release_5_5.pdf"""
types = {
    'x': "PARTY",
    'y': "AREA",
    'z': "MEASUREMENT_POINT",
    'v': "LOCATION",
    'w': "RESOURCE",
    't': "TIE_LINE",
    'a': "SUBSTATION",
}

""" taken from https://www.entsoe.eu/data/energy-identification-codes-eic/#eic-lio-websites"""
issuers = {
    "10": {"name": "ENTSOES", "country": "EU"},
    "11": {"name": "BDEW", "country": "DE"},
    "12": {"name": "Swissgrid", "country": "CH"},
    "13": {"name": "A&B", "country": "AT"},
    "14": {"name": "APCS", "country": "AT"},
    "15": {"name": "Mavir", "country": "HU"},
    "16": {"name": "REN", "country": "PT"},
    "17": {"name": "RTE", "country": "FR"},
    "18": {"name": "REE", "country": "ES"},
    "19": {"name": "PSE S.A.", "country": "PL"},
    "20": {"name": "CREOS", "country": "LU"},
    "21": {"name": "ENTSO-G", "country": ""},
    "22": {"name": "Elia", "country": "BE"},
    "23": {"name": "EFET", "country": ""},
    "24": {"name": "SEPS", "country": "SK"},
    "25": {"name": "Gas Connect", "country": "AT"},
    "26": {"name": "Terna", "country": "IT"},
    "27": {"name": "CEPS", "country": "CZ"},
    "28": {"name": "Eles", "country": "SI"},
    "29": {"name": "IPTO", "country": "GR"},
    "30": {"name": "Transelectrica", "country": "RO"},
    "31": {"name": "HOPS", "country": "HR"},
    "32": {"name": "ESO", "country": "AD"},
    "33": {"name": "MEPSO", "country": "MK"},
    "34": {"name": "EMS", "country": "RS"},
    "35": {"name": "CGES", "country": "ME"},
    "36": {"name": "NOS-BIH", "country": "BA"},
    "37": {"name": "DVGW", "country": "DE"},
    "38": {"name": "Elering", "country": "EE"},
    "39": {"name": "FGSZ", "country": "HU"},
    "40": {"name": "TEIAS", "country": "TR"},
    "41": {"name": "LITGRID", "country": "UAB"},
    "42": {"name": "EU-STREAM", "country": "SK"},
    "43": {"name": "AUGSTSPRIEGUMA", "country": "LV"},
    "44": {"name": "Fingrid Oyj", "country": "FI"},
    "45": {"name": "Energinet", "country": "DK"},
    "46": {"name": "SVK", "country": "SE"},
    "47": {"name": "Eirgrid", "country": "IE"},
    "48": {"name": "NationalGrid", "country": "UK"},
    "49": {"name": "Tennet", "country": "NL"},
    "50": {"name": "Statnett", "country": "NO"},
    "51": {"name": "Plinovodi", "country": "SI"},
    "52": {"name": "GTS", "country": "NL"},
    "53": {"name": "GAZ-SYSTEM", "country": "PL"},
    "54": {"name": "OST", "country": "AL"},
    "55": {"name": "XOSERVE", "country": "UK"},
    "56": {"name": "UKRTRANSGAZ", "country": "UA"},
    "57": {"name": "FLUXYS", "country": "BE"},
    "58": {"name": "BULGARTRANSGAZ", "country": "BG"},
    "59": {"name": "	SRG", "country": "IT"},
    "60": {"name": "	Transgaz	", "country": "RO"},
    "61": {"name": "	Conexus Baltic Grid", "country": "LV"},
    "62": {"name": "	UKRENERGO", "country": "	UA"},
    "63": {"name": "	GRTGaz", "country": "FR"},
    "64": {"name": "	Moldelectrica", "country": "	MD"},
    "65": {"name": "	GSE", "country": "GE"},
    "66": {"name": "	GasFINLAND", "country": "FI"},
    "67": {"name": "	SRBIJATRANSGAS", "country": "RS"},
    "68": {"name": "	VESTMOLDTRANSGAZ	", "country": "MD"},
    "69": {"name": "	TSOC	", "country": "CY"},
    "70": {"name": "	NOMAGAS JSC Skopje", "country": "MK"}
}

char_values = {
    '0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
    'a': 10, 'b': 11, 'c': 12, 'd': 13, 'e': 14, 'f': 15, 'g': 16, 'h': 17, 'i': 18, 'j': 19, 'k': 20, 'l': 21, 'm': 22, 'n': 23, 'o': 24, 'p': 25, 'q': 26, 'r': 27, 's': 28, 't': 29, 'u': 30, 'v': 31, 'w': 32, 'x': 33, 'y': 34, 'z': 35,
    '-': 36
}

value_chars = {v: k for k, v in char_values.items()}

def EICqm(eic_code):
    if not (len(eic_code) == 15 or len(eic_code) == 16):
        return False
    eic_code_lower = eic_code.lower()
    return all((97 <= ord(char) <= 122 or 48 <= ord(char) <= 57 or char == '-') for char in eic_code_lower)

def check_char(eic_code):
    s = eic_code[:15].lower()
    c = sum(char_values[char] * (16 - index) for index, char in enumerate(s))
    return value_chars[(36 - ((c - 1) % 37))]

def is_valid_eic(eic_code):
    return examine_eic(eic_code)['is_valid']

def examine_eic(eic_code):
    result = {
        'is_valid': True,
        'errors': [],
        'warnings': [],
        'issuer': None,
        'type': None
    }

    if len(eic_code) < 16:
        result['errors'].append({'error_message': 'TOO_SHORT'})
        result['is_valid'] = False  # set is_valid to False if code too short

    if len(eic_code) > 16:
        result['errors'].append({'error_message': 'TOO_LONG'})
        result['is_valid'] = False  # set is_valid to False if code too long

    if not eic_code.isupper():
        result['errors'].append({'error_message': 'LETTERS_LOWERCASE'})
        result['is_valid'] = False  # set is_valid to False if lowercase detcted

    if not EICqm(eic_code):  # call EICqm for validation
        result['errors'].append({'error_message': 'INVALID_FORMAT'})
        result['is_valid'] = False  # set is_valid to False if format is wrong
        return result  # malformed, so return

    eic_code = eic_code.lower()  # transform input-string to lower
    if eic_code[15] == '-':
    result['errors'].append({'error_message': 'CHECKCHAR_HYPHEN'})
    
    cc = check_char(eic_code)
    if eic_code[15] != cc:
        result['errors'].append({'error_message': 'CHECKCHAR_MISMATCH', 'error_params': [cc, eic_code[15]]})

    if eic_code[2] not in types:
        result['warnings'].append({'error_message': 'UNKNOWN_TYPE', 'error_params': [eic_code[2]]})
        result['is_valid'] = False  # set is_valid to False if type is unknown

    if eic_code[:2] not in issuers:
        result['warnings'].append({'error_message': 'UNKNOWN_ISSUER', 'error_params': [eic_code[:2]]})
        result['is_valid'] = False  # set is_valid to False if issuer is unknown

    result['issuer'] = get_issuer(eic_code)
    result['type'] = get_type(eic_code)

    return result

def get_type(eic_code):
    if not EICqm(eic_code):
        raise ValueError("Malformed EIC code")
    return types[eic_code[2]]

def get_issuer(eic_code):
    if not EICqm(eic_code):
        raise ValueError("Malformed EIC code")
    return issuers[eic_code[:2]]

def main():
    eic_code = input("Enter EIC-code to check: ")
    result = examine_eic(eic_code)
    if result['is_valid']:
        print("EIC-code is valid!")
        print("Issuer:", result['issuer'])
        print("Type:", result['type'])
    else:
        print("EIC-code is not valid!")
        print("Error:", result['errors'])

if __name__ == "__main__":
    main()
