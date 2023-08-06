#!/usr/bin/env python3
"""
Main file
"""

get_logger = __import__('filtered_logger').get_logger
PII_FIELDS = __import__('filtered_logger').PII_FIELDS

logger = get_logger()

print(type(logger))
print("PII_FIELDS: {}".format(len(PII_FIELDS)))
