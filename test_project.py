from project import user_authentication, get_balance, get_savings, get_histories
import pytest

def test_user_authentication():
    assert user_authentication("arova") == "arova"

def test_get_balance():
    assert get_balance("arova") == 0
    # if user never login before
    assert get_balance("akroma") == 0

def test_get_savings():
    assert get_savings("arova") == 0

def test_get_histories():
    assert get_histories("arova") == []