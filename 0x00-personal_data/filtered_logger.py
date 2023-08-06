#!/usr/bin/env python3
"""
Module for obfuscating sensitive data in log messages using regex.
"""

import re
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
        message = re.sub(rf'({field})=[^;]+', f'\\1={redaction}', message)
    return message


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
