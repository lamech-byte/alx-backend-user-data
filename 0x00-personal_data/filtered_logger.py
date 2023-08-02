#!/usr/bin/env python3
"""
filtered_logger.py - Module for filtering log data using regex.
"""

import os
import re
import logging
import mysql.connector


def filter_datum(fields, redaction, message, separator):
    """
    Replace occurrences of certain field values with redaction in the message.
    """
    pattern = r"(^|{0})([^{0}]*)({0}|$)".format(re.escape(separator))
    for field in fields:
        pattern = pattern.replace(field, redaction)
    return re.sub(pattern, r"\1{}\3".format(redaction), message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record):
        log_msg = super().format(record)
        return filter_datum(
            self.fields, self.REDACTION, log_msg, self.SEPARATOR
        )

# Define the PII_FIELDS constant containing the fields considered PII.


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def get_logger():
    """ Return a logger object with specific settings """
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler()
    formatter = RedactingFormatter(fields=PII_FIELDS)
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    logger.propagate = False

    return logger


def get_db():
    """ Return a connector to the database """
    db_username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    db_password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    db_host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME")

    db = mysql.connector.connect(
        user=db_username,
        password=db_password,
        host=db_host,
        database=db_name
    )

    return db


def main():
    """ Retrieve and display data from the users table """
    logger = get_logger()
    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM users;")
    for row in cursor:
        log_msg = (
            "name={}; email={}; phone={}; ssn={}; password={}; "
            "ip={}; last_login={}; user_agent={};"
        ).format(*row)
        logger.info(log_msg)

    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
