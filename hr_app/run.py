import wait_db

import logging

from hr_app import app
from config import DEBUG, LOG_FILE

if __name__ == "__main__":
    logging.basicConfig(filename=LOG_FILE, level=logging.INFO)
    app.run(host='0.0.0.0', port=5000, debug=DEBUG)
