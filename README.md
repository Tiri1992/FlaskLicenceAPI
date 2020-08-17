### Flask-Licence

Initial requirement is that you have docker installed on your machine. To check this run the following command:

```sh
$ docker --version

# Docker version 19.03.1 is the latest stable version at time of writing
```

#### Building the image using docker

Feel free to move the file into a directory of your choice and unzip the file.

First cd into the project folder.

```sh
$ cd FlaskLicence
```

Then we build the docker image.

```sh
$ docker build -t flask-licence:latest .
```

Check that the docker image is now there by doing the folllowing

```sh
$ docker images

# check to see flask-licence with tag 'latest' is there.
```

#### Running the container

Now the image has been built we can now run the application in our container. We set our port to listen on 8080. 

```sh
$ docker run -d -p 8080:8080 flask-licence:latest
```

Check our container is running by doing the following

```sh
$ docker ps
```

#### Testing our criteria

The task required two endpoints (but adapted for three endpoints):

- GET (all) with endpoint /licence

- GET driver details with endpoint adapted /licence/<licence_number: string> 

- POST send driver details with endpoint /licences

#### Request body 

Slight changes to accomidate requirements include adding a 'gender' as this impacts the licence_number (+5 for the 7th digit if female). There is also a verfication that the date is in ISOFORMAT as a string.

body -> {'first_name': string, 'middle_name': string, 'last_name': string, 'date_of_birth': string (ISOFORMAT i.e. '1997-01-13'), 'gender_male': bool}


#### REPL Example

We have our host listening on port 8080 so we could do some small checks on our local machine whilst the docker container is running. However, I am going to assume python is not installed globally. 

Instead we can go into our container and run some sanity checks alongside the test suites to verify our results. First we need to check our <CONTAINER_ID> number by doing the follwing:

```sh
$ docker ps

# check to see the CONTAINER ID of the running container named flask-licence
```

Then replace <CONTAINER_ID> with that number and run the command below.

```sh
$ docker exec -it <CONTAINER_ID> bash

# you should see the following -> root@f3d8b4c017ba:/FlaskLicence#
```

We will check by posting some data and getting some data back from our SQLite DB.

```sh
root@f3d8b4c017ba:/FlaskLicence# python

>>> import requests
>>> post_data = [{'first_name':'John', 'middle_name':'Frazer', 'last_name':'Ryan', 'date_of_birth': '1993-03-21','gender_male': True}, 
{'first_name':'Michelle', 'middle_name':None, 'last_name':'Heather', 'date_of_birth': '1974-08-03', 'gender_male':False}, 
{'first_name':'Alex', 'middle_name':None, 'last_name':'Stones', 'date_of_birth':'1968-09-23', 'gender_male':True}]

# Set our base url and add the POST endpoint "/licences"
>>> BASE = "http://localhost:8080"
>>> for data in post_data:
...     response = requests.post(BASE + "/licences", data)
...     print(response.json())

# Return results
RYAN9903213JF
HEATH708034M9
STONE609238A9
```
Sending a get requests to retrieve a list of **all** data with the endpoint "/licence"
```sh
>>> response = requests.get(BASE + "/licence")
>>> response
<Response [200]>
>>> response.json()
['HEATH708034M9', 'RYAN9903213JF', 'STONE609238A9']
```

Now we know some of the licence_numbers we can requests individual drivers using the extension /licence/<licence_number: string> and will return a dictionary of field:value pairs from the DB.

```sh
>>> response = requests.get(BASE + "/licence/HEATH708034M9")
>>> response.json()
{'id': 2, 'first_name': 'Michelle', 'middle_name': None, 'last_name': 'Heather', 'date_of_birth': '1974-08-03', 'gender_male': True, 'licence_number': 'HEATH708034M9'}
```

### Test suite

There are two test scripts (tests/test.py, tests/test_client.py).

- test/test.py: Tests the class NamesToLicence which aims to convert user details into licence_number based on the information provided https://ukdriving.org.uk/licencenumber.html

- test/test_client.py: Tests various GET/POST requests. 

```sh
root@f3d8b4c017ba:/FlaskLicence# cd tests

root@f3d8b4c017ba:/FlaskLicence/tests# pytest test.py -v
=================================================== test session starts ===================================================
platform linux -- Python 3.8.5, pytest-6.0.1, py-1.9.0, pluggy-0.13.1 -- /usr/local/bin/python
cachedir: .pytest_cache
rootdir: /FlaskLicence/tests
collected 7 items                                                                                                         

test.py::TestNamesToLicence::test_first_five_small PASSED                                                           [ 14%]
test.py::TestNamesToLicence::test_first_five_large PASSED                                                           [ 28%]
test.py::TestNamesToLicence::test_date_format PASSED                                                                [ 42%]
test.py::TestNamesToLicence::test_second_six PASSED                                                                 [ 57%]
test.py::TestNamesToLicence::test_last_two PASSED                                                                   [ 71%]
test.py::TestNamesToLicence::test_convert PASSED                                                                    [ 85%]
test.py::TestLicenceModel::test_new_driver PASSED                                                                   [100%]

root@f3d8b4c017ba:/FlaskLicence/tests# pytest test_client.py -v
=================================================== test session starts ===================================================
platform linux -- Python 3.8.5, pytest-6.0.1, py-1.9.0, pluggy-0.13.1 -- /usr/local/bin/python
cachedir: .pytest_cache
rootdir: /FlaskLicence/tests
collected 3 items                                                                                                         

test_client.py::TestRequests::test_get_request PASSED                                                               [ 33%]
test_client.py::TestRequests::test_get_all_licence_requests PASSED                                                  [ 66%]
test_client.py::TestRequests::test_post_request PASSED                                                              [100%]
```