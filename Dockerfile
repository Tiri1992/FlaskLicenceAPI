# Set base image
FROM python:3.8

# Set the working directory
WORKDIR /FlaskLicence

# Copy just the requirements
COPY ./requirements.txt /FlaskLicence/requirements.txt

# Install requirements
RUN pip install -r requirements.txt

# Copy source code & tests in stages
COPY ./App /FlaskLicence/App

COPY ./tests /FlaskLicence/tests

COPY ./run.py /FlaskLicence/run.py

# Expose port 8080
EXPOSE 8080

CMD ["python", "./run.py"]
