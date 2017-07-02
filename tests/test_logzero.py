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

        # with open(temp.name) as f:
        #     content = f.read()
        #     # assert str(testbytes) in content

    finally:
        temp.close()


def test_unicode():
    """
    Should log unicode
    """
    temp = tempfile.NamedTemporaryFile()
    try:
        logger = logzero.setup_logger(logfile=temp.name)

        logger.debug("😄 😁 😆 😅 😂")

        with open(temp.name, "rb") as f:
            content = f.read()
            assert "\\xf0\\x9f\\x98\\x84 \\xf0\\x9f\\x98\\x81 \\xf0\\x9f\\x98\\x86 \\xf0\\x9f\\x98\\x85 \\xf0\\x9f\\x98\\x82\\n" in repr(content)

    finally:
        temp.close()


def test_multiple_loggers_one_logfile():
    """
    Should properly log bytes
    """
    temp = tempfile.NamedTemporaryFile()
    try:
        logger1 = logzero.setup_logger(name="logger1", logfile=temp.name)
        logger2 = logzero.setup_logger(name="logger2", logfile=temp.name)
        logger3 = logzero.setup_logger(name="logger3", logfile=temp.name)

        logger1.info("logger1")
        logger2.info("logger2")
        logger3.info("logger3")

        with open(temp.name) as f:
            content = f.read().strip()
            assert "logger1" in content
            assert "logger2" in content
            assert "logger3" in content
            assert len(content.split("\n")) == 3

    finally:
        temp.close()


def test_default_logger():
    """
    Default logger should work and be able to be reconfigured.
    """
    temp = tempfile.NamedTemporaryFile()
    try:
        logzero.setup_default_logger(logfile=temp.name)
        logzero.logger.debug("debug1")  # will be logged

        # Setup with loglevel INFO
        logzero.setup_default_logger(logfile=temp.name, level=logging.INFO)
        logzero.logger.debug("debug2")  # will not be logged

        logzero.logger.info("info1")  # will be logged

        # Setup a different formatter
        log_format = '%(color)s[xxx]%(end_color)s %(message)s'
        formatter = logzero.LogFormatter(fmt=log_format)
        logzero.setup_default_logger(logfile=temp.name, level=logging.INFO, formatter=formatter)

        logzero.logger.info("info2")  # will be logged with new formatter
        logzero.logger.debug("debug3")  # will not be logged

        with open(temp.name) as f:
            content = f.read()
            assert "] debug1" in content
            assert "] debug2" not in content
            assert "] info1" in content
            assert "xxx] info2" in content
            assert "] debug3" not in content

    finally:
        temp.close()
