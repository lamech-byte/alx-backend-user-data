#!/usr/bin/env python3
"""
filtered_logger.py - Module for filtering log data using regex.
"""

import re


def filter_datum(fields, redaction, message, separator):
    """
    Replace occurrences of certain field values with redaction in the message.
    """
    pattern = r"(^|{0})([^{0}]*)({0}|$)".format(re.escape(separator))
    for field in fields:
        pattern = pattern.replace(field, redaction)
    return re.sub(pattern, r"\1{}\3".format(redaction), message)
