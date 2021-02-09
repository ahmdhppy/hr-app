import hashlib
import os
import logging

from datetime import datetime

import boto3
from botocore.exceptions import NoCredentialsError

from hr_app import db
from config import FILE_STORE_PATH, FILE_STORE_METHOD, \
                 ACCESS_KEY_AWS, SECRET_KEY_AWS, BUCKET_AWS

_logger = logging.getLogger(__name__)


class Candidate(db.Model):
    __tablename__ = 'candidate'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    yoe = db.Column(db.Float, nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    reg_date = db.Column(db.DateTime, nullable=False)
    file = db.Column(db.Text, nullable=False)
    file_name = db.Column(db.Text, nullable=False)
    department = db.Column(db.Text, nullable=False)
    
    @property
    def get_file_path(self):
        """
        Get the absolute path for resume file.
        """
        return os.path.join(FILE_STORE_PATH, self.file)
    
    



    @classmethod
    def save_file_aws(cls, file, file_name):
        """
        Save the resume to AWS.
        """
        bucket = BUCKET_AWS
        s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY_AWS,
                          aws_secret_access_key=SECRET_KEY_AWS)
    
        try:
            s3.upload_file(file, bucket, file_name)
            _logger.info("Upload Successful")
            return True
        except FileNotFoundError:
            _logger.info("The file was not found")
            return False
        except NoCredentialsError:
            _logger.info("Credentials not available")
            return False
    
    @classmethod
    def save_file_local(cls, file, file_name):
        """
        Save the resume to local storage.
        """
        file.stream.seek(0)
        file_path = os.path.join(FILE_STORE_PATH, file_name)
        file.save(file_path)
        return file_path
    
    @classmethod
    def create(cls, vals):
        """
        Creates a record with given values.
        """
        _logger.info("Creating new Candidate.")
        
        missing_fields = [field for field in ['name', 'yoe', 'birth_date', 'file', 'department'] if not vals.get(field)]
        if missing_fields:
            return f"The following fields are required: {', '.join(missing_fields)}"
        
        dep_val = ['IT', 'HR', 'Finance']
        if vals['department'] not in dep_val:
            return f"The department value should be one of the following values: {', '.join(dep_val)} "
            
        file = vals['file']
        if file.mimetype not in ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']:
            return 'The file should be PDF or DOCX.'
        
        file_sha1 = hashlib.sha1(file.read()).hexdigest()
        
        getattr(cls, 'save_file_' + FILE_STORE_METHOD)(file, file_sha1)
        
        vals['file_name'] = file.filename
        vals['file'] = file_sha1
        vals['reg_date'] = datetime.now()
        
        record = cls(**vals)
        db.session.add(record)
        db.session.commit()
        return record
    
