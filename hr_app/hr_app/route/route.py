import logging

from functools import wraps
from pprint import pformat

from flask import  render_template, request, send_file

from hr_app import app
from ..models.models import Candidate

_logger = logging.getLogger(__name__)


def is_admin(func):
    """
    Check if the user is admin.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        x_admin = request.headers.get('X-ADMIN')
        if not x_admin or int(x_admin) != 1:
            _logger.info("Unauthorized access to '%s' from: %s." % (func.__name__, request.remote_addr))
            return "Unauthorized access"
        return func(*args, **kwargs)

    return wrapper


@app.route('/v1/download/resume/<int:id>', methods=['GET'])
@is_admin
def download_resume(id):
    """
    Download resume API
    """
    _logger.info("Downloading resume for candidate ID: %s." % id)
    candidate = Candidate.query.get(id)
    if not candidate:
        return "The candidate does not exist!"
    return send_file(candidate.get_file_path,
                    attachment_filename=candidate.file_name,
                    as_attachment=True)

        
@app.route('/v1/applicants', methods=['GET'])
@is_admin
def get_applicants():
    """
    List all applicants API
    """
    _logger.info("List all applicants.")
    candidates = Candidate.query.order_by(Candidate.reg_date.desc()).all()
    rows = [{'id':candidate.id,
              'name':candidate.name,
              'birth_date':candidate.birth_date.strftime('%d/%m/%Y'),
              'yoe':candidate.yoe,
              'department':candidate.department} for candidate in candidates]
    return pformat(rows)
    

@app.route('/v1/create/candidate', methods=['POST'])
def create_candidate():
    """
    Create candidate API
    """
    vals = dict(request.form)
    vals['file'] = request.files.get('file')
    result = Candidate.create(vals)
    return isinstance(result, str) and {'success':False, 'msg':result}  or {'success':True, 'msg':'The record has created'}
