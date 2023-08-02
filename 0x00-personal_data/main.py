#!/usr/bin/env python3
"""
Main file
"""

import logging
from filtered_logger import RedactingFormatter

# Create a logger and set its level
logger = logging.getLogger('my_logger')
logger.setLevel(logging.INFO)

# Create a stream handler with the RedactingFormatter
handler = logging.StreamHandler()
handler.setFormatter(RedactingFormatter(fields=("email", "ssn", "password")))

# Add the handler to the logger
logger.addHandler(handler)

message = "name=Bob;email=bob@dylan.com;ssn=000-123-0000;password=bobby2019;"

# Log the message using the configured logger
logger.info(message)
