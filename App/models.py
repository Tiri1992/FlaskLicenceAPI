from App import db
# Licence Table


class LicenceModel(db.Model):
    """Constructor mapping to Licences Table."""
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    middle_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    gender_male = db.Column(db.Boolean, nullable=False)
    licence_number = db.Column(db.String(13), nullable=False, unique=True)

    def __repr__(self) -> str:
        return f"LicenceModel(first_name={first_name}, last_name={last_name}, date_of_birth={date_of_birth})"
