"""
Tools used to convert name into driving licence
"""
from datetime import datetime
import re
# user defined exceptions


class IncorrectDateFormat(Exception):
    """Raised when time format is incorrect."""


class NameToLicence:
    """
    Converts Firstname, Lastname, DOB -> Driving Licence Number.
    """

    def __init__(self, firstname: str, middlename: str, lastname: str, dob: str) -> None:
        self.firstname = firstname
        self.middelname = middlename
        self.lastname = lastname
        self.dob = dob

    @staticmethod
    def double_barrelled_names(name: str) -> str:
        """
        Cleans double barreled names to a format eligible to
        be processed for the .first_five() method.
        """
        split = re.split(r"-|\s|_", name)
        if len(split) > 1:
            # Double barreled
            return ''.join(split)
        else:
            return name

    @property
    def date(self) -> datetime:
        try:
            date_obj = datetime.fromisoformat(self.dob)
        except ValueError:
            # Wanted to implement a user-defined exception here.
            raise IncorrectDateFormat(
                "Incorrect date format. Must be of type YYYY-MM-DD.")
        return date_obj

    def first_five(self) -> str:
        """Adjusts for the first 5 elements"""
        # helper function for elements 1-5:
        lastname_clean = NameToLicence.double_barrelled_names(self.lastname)
        lastname_adj = lastname_clean.ljust(5, '9').upper()[:5]
        return lastname_adj

    def second_six(self, male: bool) -> str:
        """
        Adjusts for the next 6 elements.

        Parameters:
        -----------
        male: bool, This represents users gender.
        """
        # helper function for elements 6-11
        decade = str(self.date.year)[-2]
        day = str(self.date.day).rjust(2, '0')
        year_of_birth = str(self.date.year)[-1]
        if male:
            month = str(self.date.month).rjust(2, '0')
            # Concat strings:
            result = ''.join([decade, month, day, year_of_birth])
            return result
        else:
            # If female, second digit must end in 5 (for months Jan - Sept) or 6 (for Nov - Dec)
            month = str(self.date.month + 50)
            # Concat strings:
            result = ''.join([decade, month, day, year_of_birth])
            return result

    def last_two(self) -> str:
        """Adjusts for the last two elements of the 13 needed to be processed."""
        # Helper function for elements 12-13
        if not self.middelname:
            # User has no middle name
            return self.firstname[0].upper() + '9'
        else:
            return self.firstname[0].upper() + self.middelname[0].upper()

    def convert(self, male: bool) -> str:
        """Returns processed Driving Licence Number"""
        if male:
            result = self.first_five() + self.second_six(male=True) + self.last_two()
            return result
        else:
            result = self.first_five() + self.second_six(male=False) + self.last_two()
            return result
