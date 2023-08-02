#!/usr/bin/env python3
"""
filtered_logger.py - Module for filtering log data using regex.
"""

import logging
import re
from typing import List


def filter_datum(
    fields: List[str], redaction: str, message: str, separator: str
) -> str:
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

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        log_msg = super().format(record)
        return filter_datum(self.fields, self.REDACTION, log_msg, self.SEPARATOR)

# Define the PII_FIELDS constant containing the fields considered PII.
PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')

def get_logger() -> logging.Logger:
    """ Return a logger object with specific settings """
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler()
    formatter = RedactingFormatter(fields=PII_FIELDS)
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    logger.propagate = False

    return logger
