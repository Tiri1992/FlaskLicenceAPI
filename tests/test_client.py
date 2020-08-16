"""
Test: Post/Get requests
"""
import pytest
from .context import app
from .context import db
from .context import LicenceModel
from datetime import datetime


@pytest.fixture
def test_client():
    """
    Client fixture will be called by each individual test.
    """
    testing_client = app.test_client()

    # Establish an application context before running the tests
    ctx = app.app_context()
    ctx.push()

    yield testing_client

    # remove when finished
    ctx.pop()


@pytest.fixture
def init_db():
    # Create the db (overwrites existing) and table
    db.create_all()

    # Insert some drivers data:
    data1 = {'first_name': 'George',
             'middle_name': 'James',
             'last_name': 'Hillmans',
             'date_of_birth': datetime(1988, 3, 4),
             'gender_male': True,
             'licence_number': 'HILLM803048GJ'}
    data2 = {'first_name': 'Anna',
             'middle_name': None,
             'last_name': 'Matello',
             'date_of_birth': datetime(1996, 8, 23),
             'gender_male': False,
             'licence_number': 'MATEL958236A9'}
    driver1 = LicenceModel(**data1)
    driver2 = LicenceModel(**data2)
    db.session.add(driver1)
    db.session.add(driver2)

    # commit changes
    db.session.commit()

    # yield database
    yield db

    # tear down when finished!
    db.drop_all()


class TestRequests:

    def test_get_request(self, test_client, init_db):
        """
        Test get request from DB to get details of driver
        using the licence_number.
        """
        response = test_client.get("/licence/HILLM803048GJ")
        driver_json = response.json
        assert response.status_code == 200
        assert driver_json.get('last_name') == 'Hillmans'
        # Isoformat date is recieved back as a str because db is SQLite
        assert driver_json.get('date_of_birth') == '1988-03-04'
        assert driver_json.get('gender_male') == True
        assert driver_json.get('licence_number') == 'HILLM803048GJ'

    def test_get_all_licence_requests(self, test_client, init_db):
        """
        Test gets ALL licence_numbers from DB and returns a list of
        all licence_numbers.
        """
        response = test_client.get("/licence")
        assert response.status_code == 200
        assert isinstance(eval(response.get_data()), list)
        assert eval(response.get_data()) == ['HILLM803048GJ', 'MATEL958236A9']

    def test_post_request(self, test_client, init_db):
        """
        Test post request to DB. 

        Returns a 13 digit licence_number as a string.
        """
        # Note that the LicencePOST.post() method handles licence_number
        driver3 = {'first_name': 'Floyd',
                   'middle_name': 'Dunn',
                   'last_name': 'Mayweather',
                   'date_of_birth': '1977-02-24',
                   'gender_male': True
                   }
        response = test_client.post("/licences", json=driver3)
        assert response.is_json
        assert isinstance(response.content_type, str)
        assert response.status_code == 200
        # Returns a 13 digit licence_number
        # Eval turns bytes -> str
        assert eval(response.data) == "MAYWE702247FD"
