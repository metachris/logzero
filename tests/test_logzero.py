#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_logzero
----------------------------------

Tests for `logzero` module.
"""
import tempfile
import logzero


def test_write_to_logfile():
    """Sample pytest test function with the pytest fixture as an argument.
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
    """Sample pytest test function with the pytest fixture as an argument.
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
