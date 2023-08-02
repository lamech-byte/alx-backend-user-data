#!/usr/bin/env python3
"""
filtered_logger.py - Module for filtering log data using regex.
"""

import re

def filter_datum(fields, redaction, message, separator):
    """
    Replace occurrences of certain field values with redaction in the message.
    """
    return re.sub(
        r"(?<=^|{})(?:(?<=\{})[^{}]*(?=\{})|[^{}]*)(?=$|{}
        )".format(separator, separator, separator, separator, separator, redaction), message)
