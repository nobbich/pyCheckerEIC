# test_eic.py

import pytest
from eic_validator import get_issuer

from eic_validator import examine_eic

def test_valid_eic():
    result = examine_eic("12X-0000001502-P")
    assert result['is_valid'] == True

def test_invalid_eic():
    result = examine_eic("abc")
    assert result['is_valid'] == False

def test_invalid_length_short():
    result = examine_eic("12X-0001502-P")
    assert result['errors'][0]['error_message'] == 'TOO_SHORT'

def test_invalid_length_long():
    result = examine_eic("12X-000159993302-P")
    assert result['errors'][0]['error_message'] == 'TOO_LONG'

def test_lowercase_letters():
    result = examine_eic("12x-0000001502-p")
    assert result['errors'][0]['error_message'] == 'LETTERS_LOWERCASE'

def test_testchar_mismatch():
    result = examine_eic("12X-0000001502-D")
    assert result['errors'][0]['error_message'] == 'CHECKCHAR_MISMATCH'

def test_testchar_hyphen():
    result = examine_eic("12X-0000001502--")
    assert result['errors'][0]['error_message'] == 'CHECKCHAR_HYPHEN'   
