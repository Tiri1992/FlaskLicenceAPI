"""
Test Suite for tools.py

Questionable edge cases to discuss:

- Two users same names/gender born on 1900-01-01 and 2000-01-01 will have identical licence numbers.
"""
from tools import NameToLicence
from tools import IncorrectDateFormat
import pytest


@pytest.fixture
def user_input_small_init():
    """Female User"""
    firstname = "Jane"
    middlename = "Brie"
    lastname = "Doe"
    dob = "1997-03-26"
    return NameToLicence(firstname, middlename, lastname, dob)


@pytest.fixture
def user_input_large_init():
    """Male User"""
    firstname = "Gary"
    middlename = None
    lastname = "Lineker"
    dob = "1960-11-30"
    return NameToLicence(firstname, middlename, lastname, dob)


@pytest.fixture
def user_input_edge_case_1_init():
    """Male with double barrelled last name"""
    firstname = "Richard"
    middlename = "May"
    lastname = "An-John"
    dob = "1988-04-28"
    return NameToLicence(firstname, middlename, lastname, dob)


@pytest.fixture
def user_input_edge_case_2_init():
    """Female with double barrelled last name"""
    firstname = "Christina"
    middlename = "Jay-Wise"
    lastname = "C-Tri"
    dob = "1968-07-12"
    return NameToLicence(firstname, middlename, lastname, dob)


@pytest.fixture
def user_input_incorrect_date_init():
    firstname = "Jimmy"
    middlename = "Mike"
    lastname = "Christakis"
    dob = "1998-16-03"
    return NameToLicence(firstname, middlename, lastname, dob)


class TestNamesToLicence:

    def test_first_five_small(self, user_input_small_init):
        assert user_input_small_init.first_five() == "DOE99"

    def test_first_five_large(self, user_input_large_init, user_input_edge_case_1_init, user_input_edge_case_2_init):
        assert user_input_large_init.first_five() == "LINEK"
        assert user_input_edge_case_1_init.first_five() == "ANJOH"
        assert user_input_edge_case_2_init.first_five() == "CTRI9"

    def test_date_format(self, user_input_incorrect_date_init):
        ntl_user = user_input_incorrect_date_init
        try:
            date = ntl_user.date
        except IncorrectDateFormat as err:
            # check message of error is correct
            assert err.args[0] == "Incorrect date format. Must be of type YYYY-MM-DD."

    def test_second_six(self, user_input_small_init, user_input_large_init):
        assert user_input_small_init.second_six(male=False) == "953267"
        assert user_input_large_init.second_six(male=True) == "611300"

    def test_last_two(self, user_input_small_init, user_input_large_init):
        assert user_input_small_init.last_two() == "JB"
        assert user_input_large_init.last_two() == "G9"

    def test_convert(self, user_input_small_init, user_input_large_init, user_input_edge_case_1_init, user_input_edge_case_2_init):
        assert user_input_small_init.convert(male=False) == "DOE99953267JB"
        assert user_input_large_init.convert(male=True) == "LINEK611300G9"
        assert user_input_edge_case_1_init.convert(
            male=True) == "ANJOH804288RM"
        assert user_input_edge_case_2_init.convert(
            male=False) == "CTRI9657128CJ"
