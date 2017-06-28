#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_logzero
----------------------------------

Tests for `logzero` module.
"""
import os
import tempfile
import logging
import logzero


def test_write_to_logfile():
    """
    Should log to a file.
    """
    temp = tempfile.NamedTemporaryFile()
    try:
        logger = logzero.setup_logger(logfile=temp.name)
        logger.info("test log output")

        with open(temp.name) as f:
            content = f.read()
            assert " test_logzero:" in content
            assert content.endswith("test log output\n")

    finally:
        temp.close()

def test_custom_formatter():
    """
    Should work with a custom formatter.
    """
    temp = tempfile.NamedTemporaryFile()
    try:
        log_format = '%(color)s[%(levelname)1.1s %(asctime)s customnametest:%(lineno)d]%(end_color)s %(message)s'
        formatter = logzero.LogFormatter(fmt=log_format)
        logger = logzero.setup_logger(logfile=temp.name, formatter=formatter)
        logger.info("test log output")

        with open(temp.name) as f:
            content = f.read()
            assert " customnametest:" in content
            assert content.endswith("test log output\n")

    finally:
        temp.close()

def test_loglevel():
    """
    Should not log any debug messages if minimum level is set to INFO
    """
    temp = tempfile.NamedTemporaryFile()
    try:
        logger = logzero.setup_logger(logfile=temp.name, level=logging.INFO)
        logger.debug("test log output")

        with open(temp.name) as f:
            content = f.read()
            assert len(content.strip()) == 0

    finally:
        temp.close()

def test_bytes():
    """
    Should properly log bytes
    """
    temp = tempfile.NamedTemporaryFile()
    try:
        logger = logzero.setup_logger(logfile=temp.name)

        testbytes = os.urandom(20)
        logger.debug(testbytes)
        logger.debug(None)

        with open(temp.name) as f:
            content = f.read()
            # assert str(testbytes) in content

    finally:
        temp.close()
