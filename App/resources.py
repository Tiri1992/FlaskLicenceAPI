from flask_restful import Resource, reqparse, abort, fields, marshal_with
from App.tools import NameToLicence
from App.models import LicenceModel
from datetime import datetime

# Import api in package
from App import api
from App import db

# type hints
from typing import List, Tuple, Dict, Union

# RequestParser adds regulation to our parsed arguments.
licence_post_args = reqparse.RequestParser()
licence_post_args.add_argument(
    "first_name", type=str, help="First name required", required=True)
licence_post_args.add_argument(
    "middle_name", type=str, help="Middle name required")
licence_post_args.add_argument(
    "last_name", type=str, help="Last name required", required=True)
licence_post_args.add_argument(
    "date_of_birth", type=datetime.fromisoformat, help="Date of birth required is YYYY-MM-DD format", required=True)
licence_post_args.add_argument(
    "gender_male", type=bool, help="Gender required", required=True)
licence_post_args.add_argument(
    "licence_number", type=str, help="13 digit Licence number.")

# Resource field to tell how an object queried from db should be serialised
resource_field = {
    'id': fields.Integer,
    'first_name': fields.String,
    'middle_name': fields.String,
    'last_name': fields.String,
    'date_of_birth': fields.String,
    'gender_male': fields.Boolean,
    'licence_number': fields.String
}

# Create a class that inherits from resource and overwrite GET, POST requests


class LicenceGET(Resource):
    @marshal_with(resource_field)
    def get(self, licence_number: str) -> Tuple[Dict[str, Union[str,int]], int]:
        """
        GET request from database.

        Parameters
        ----------
        licence_number
            Unique identifier of driver.

        Returns
        -------
        dict
            single row of fields from db in the form of fields: value.
        """
        result = LicenceModel.query.filter_by(
            licence_number=licence_number).first()
        if not result:
            # No user with this licence number: http 404 - Not Found
            abort(404, message="Could not find licence_number.")
        return result, 200


class LicenceGETALL(Resource):
    def get(self) -> Tuple[List[str], int]:
        """
        GET all licences available from database.

        Returns
        -------
        list
            A list of all licence_numbers in db.
        """
        # Get all licence_numbers available
        result = db.session.query(LicenceModel.licence_number)
        if not result:
            # No user with this licence number: http 404 - Not Found
            abort(404, message="Database is empty.")
        # Using a listcomp to extract relevant data
        # Uniqueness is guarenteed from table schema
        results_list = [val[0] for val in result]
        return results_list, 200


class LicencePOST(Resource):
    def post(self) -> str:
        """
        POST request to database. Adapted task to include gender
        as this influences the Drivers Licence ID.

        Request body: {
            'first_name': str,
            'middle_name': str,
            'last_name': str,
            'date_of_birth': str,
            'gender_male': bool
        }

        Returns
        -------
        str
            Will return a 13 digit licence_number with 
            respect to the input request body.
        """
        # Parse our arguments so we can access them and persist new data to our db
        args = licence_post_args.parse_args()
        # Generate Licence Number
        ntl = NameToLicence(
            first_name=args['first_name'], middle_name=args['middle_name'], last_name=args['last_name'], date_of_birth=args['date_of_birth'])
        gen_licence_num = ntl.convert(male=args['gender_male'])
        # Validate length of names to be up to 50 characters: First_name, Last_name
        if not all(map(lambda row: 0 < len(row) <= 50, [args['first_name'], args['last_name']])):
            abort(400, message="First and Last name should be between 1 and 50 characters.")
        # Validate length of middle name: This is optional so can take None, but need to check if str is parsed
        if not args['middle_name']:
            if not (0 < len(args['middle_name']) <= 50):
                abort(400, message="Middle name can either be blank or up to 50 characters long.")
        # Check database if licence number already exists
        result = LicenceModel.query.filter_by(
            licence_number=gen_licence_num).first()
        if result:
            # Abort the Post request as driver already in DB: 409 error conflict
            abort(409, message="Licence already exists.")
        # Update args with licence number generated
        args['licence_number'] = gen_licence_num
        # Create a new instance
        new_data = LicenceModel(**args)
        # Add to DB and commit:
        db.session.add(new_data)
        db.session.commit()
        # Return Licence number as string
        return gen_licence_num


# add path to api: Added additional resource to get specific licence_numbers
api.add_resource(LicenceGET, "/licence/<string:licence_number>")
api.add_resource(LicenceGETALL, "/licence")
api.add_resource(LicencePOST, "/licences")
