#!/usr/bin/env python3
"""
filtered_logger.py - Module for filtering log data using regex.
"""

import re

def filter_datum(fields, redaction, message, separator):
    """
    Replace occurrences of certain field values with redaction in the message.
    """
    pattern = r"(?<=^|{})(?:(?<=\{})[^{}]*(?=\{})|[^{}]*)(?=$|{})".format(
        separator, separator, separator, separator, separator, redaction
    )
    return re.sub(pattern, redaction, message)
