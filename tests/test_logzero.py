#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_logzero
----------------------------------

Tests for `log0` module.
"""

import pytest
import tempfile

from logzero import setup_logger


def test_write_to_logfile():
    """Sample pytest test function with the pytest fixture as an argument.
    """
    temp = tempfile.NamedTemporaryFile()
    try:
        logger = setup_logger(logfile=temp.name)
        logger.info("test log output")

        with open(temp.name) as f:
            content = f.read()
            assert content.endswith("test log output\n")

    finally:
        temp.close()
