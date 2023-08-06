#!/usr/bin/env python3
"""
Module for obfuscating sensitive data in log messages using regex.
"""

import re
import logging
from typing import List


def filter_datum(
    fields: List[str], redaction: str, message: str, separator: str
) -> str:
    """
    Obfuscate sensitive fields in the log message using regex substitution.

    Args:
        fields (List[str]): List of fields to obfuscate.
        redaction (str): String to replace the obfuscated fields.
        message (str): The log message containing fields to obfuscate.
        separator (str): Character separating fields in the log message.

    Returns:
        str: The obfuscated log message.
    """
    for field in fields:
        message = re.sub(
            rf'({field})=[^{separator}]+', f'\\1={redaction}', message
        )
    return message


class RedactingFormatter(logging.Formatter):
    """
    Custom log formatter for redacting sensitive data.

    Args:
        fields (List[str]): List of fields to obfuscate.

    Attributes:
        REDACTION (str): String to replace the obfuscated fields.
        FORMAT (str): Log message format.
        SEPARATOR (str): Character separating fields in the log message.

    Methods:
        format(record: logging.LogRecord) -> str:
            Formats the log record while redacting specified fields.
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super().__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Formats the log record while redacting specified fields.

        Args:
            record (logging.LogRecord): The log record to be formatted.

        Returns:
            str: The formatted log message with sensitive fields redacted.
        """
        message = super().format(record)
        return filter_datum(
            self.fields, self.REDACTION, message, self.SEPARATOR
        )


def get_logger():
    """
    Get a logger named "user_data" that logs up to logging.INFO level.
    The logger has a StreamHandler with RedactingFormatter as formatter.
    
    Returns:
        logging.Logger: A logger instance.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    
    handler = logging.StreamHandler()
    formatter = RedactingFormatter(fields=PII_FIELDS)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    return logger


# Constants
PII_FIELDS = ("name", "email", "phone", "address", "credit_card")


if __name__ == "__main__":
    fields = ["password", "date_of_birth"]
    messages = [
        "name=egg;email=eggmin@eggsample.com;"
        "password=eggcellent;date_of_birth=12/12/1986;",
        "name=bob;email=bob@dylan.com;"
        "password=bobbycool;date_of_birth=03/04/1993;"
    ]

    for message in messages:
        print(filter_datum(fields, 'xxx', message, ';'))
