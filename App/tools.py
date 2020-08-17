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
    The NameToLicence object contains details of the driver.
    Methods available such as .convert() outputs Licence Number.

    Parameters
    ----------
    firstname
        First name of driver.

    middlename
        Middle name of driver.

    lastname
        Last name of driver.

    date_of_birth : str
        Drivers date of birth.

    Returns
    -------
    None
    """

    def __init__(self, first_name: str, middle_name: str, last_name: str, date_of_birth: str) -> None:
        self.firstname = first_name
        self.middelname = middle_name
        self.lastname = last_name
        self.dob = date_of_birth

    @staticmethod
    def double_barrelled_names(name: str) -> str:
        """
        Cleans double barreled names to a format eligible to
        be processed for the .first_five() method.

        Parameters
        ----------
        name
            Double barrelled name to be concatenated.

        Returns
        -------
        str
            The name of driver is concatenated into a single string.
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
            date_obj = datetime.fromisoformat(str(self.dob))
        except ValueError:
            # Wanted to implement a user-defined exception here.
            raise IncorrectDateFormat(
                "Incorrect date format. Must be of type YYYY-MM-DD.")
        return date_obj

    def first_five(self) -> str:
        """
        Processes elements 1 - 5 of the licence number

        Returns
        -------
        str
            Elements 1 - 5 of the licence number.
        """
        # helper function for elements 1-5:
        lastname_clean = NameToLicence.double_barrelled_names(self.lastname)
        lastname_adj = lastname_clean.ljust(5, '9').upper()[:5]
        return lastname_adj

    def second_six(self, male: bool) -> str:
        """
        Processes elements 6 - 11 of the licence number

        Parameters
        ----------
        male
            This represents users gender.

        Returns
        -------
        str
            Elements 6 - 11 of the licence number.
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
        """
        Processes elements 12 - 13 of the licence number.
        
        Returns
        -------
        str
            Elements 12 - 13 of the licence number.
        """
        # Helper function for elements 12-13
        if not self.middelname:
            # User has no middle name
            return self.firstname[0].upper() + '9'
        else:
            return self.firstname[0].upper() + self.middelname[0].upper()

    def convert(self, male: bool) -> str:
        """
        Converts driver details into licence_number entirely.
        
        Parameters
        ----------
        male
            If driver is male.
        
        Returns
        -------
        str
            Licence number of the driver details passed into constructor.
        """
        if male:
            result = self.first_five() + self.second_six(male=True) + self.last_two()
            return result
        else:
            result = self.first_five() + self.second_six(male=False) + self.last_two()
            return result
