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


def test_api_logfile(capsys):
    """
    logzero.logfile(..) should work as expected
    """
    logzero.reset_default_logger()
    temp = tempfile.NamedTemporaryFile()
    try:
        logzero.logger.info("info1")

        # Set logfile
        logzero.logfile(temp.name)
        logzero.logger.info("info2")

        # Remove logfile
        logzero.logfile(None)
        logzero.logger.info("info3")

        # Set logfile again
        logzero.logfile(temp.name)
        logzero.logger.info("info4")

        with open(temp.name) as f:
            content = f.read()
            assert "] info1" not in content
            assert "] info2" in content
            assert "] info3" not in content
            assert "] info4" in content

    finally:
        temp.close()


def test_api_loglevel(capsys):
    """
    Should reconfigure the internal logger loglevel
    """
    logzero.reset_default_logger()
    temp = tempfile.NamedTemporaryFile()
    try:
        logzero.logfile(temp.name)
        logzero.logger.info("info1")
        logzero.loglevel(logging.WARN)
        logzero.logger.info("info2")
        logzero.logger.warn("warn1")

        with open(temp.name) as f:
            content = f.read()
            assert "] info1" in content
            assert "] info2" not in content
            assert "] warn1" in content

    finally:
        temp.close()


def test_api_loglevel_custom_handlers(capsys):
    """
    Should reconfigure the internal logger loglevel and custom handlers
    """
    logzero.reset_default_logger()
    # TODO
    pass
    # temp = tempfile.NamedTemporaryFile()
    # try:
    #     logzero.logfile(temp.name)
    #     logzero.logger.info("info1")
    #     logzero.loglevel(logging.WARN)
    #     logzero.logger.info("info2")
    #     logzero.logger.warn("warn1")

    #     with open(temp.name) as f:
    #         content = f.read()
    #         assert "] info1" in content
    #         assert "] info2" not in content
    #         assert "] warn1" in content

    # finally:
    #     temp.close()


def test_api_rotating_logfile(capsys):
    """
    logzero.rotating_logfile(..) should work as expected
    """
    logzero.reset_default_logger()
    temp = tempfile.NamedTemporaryFile()
    try:
        logzero.logger.info("info1")

        # Set logfile
        logzero.logfile(temp.name, maxBytes=10, backupCount=3)
        logzero.logger.info("info2")
        logzero.logger.info("info3")

        with open(temp.name) as f:
            content = f.read()
            assert "] info1" not in content  # logged before setting up logfile
            assert "] info2" not in content  # already rotated out
            assert "] info3" in content  # already rotated out

        fn_rotated = temp.name + ".1"
        assert os.path.exists(fn_rotated)
        with open(fn_rotated) as f:
            content = f.read()
            assert "] info2" in content

    finally:
        temp.close()


def test_api_logfile_custom_loglevel():
    """
    logzero.logfile(..) should be able to use a custom loglevel
    """
    logzero.reset_default_logger()
    temp = tempfile.NamedTemporaryFile()
    try:
        # Set logfile with custom loglevel
        logzero.logfile(temp.name, loglevel=logging.WARN)
        logzero.logger.info("info1")
        logzero.logger.warn("warn1")

        # If setting a loglevel with logzero.loglevel(..) it will not overwrite
        # the custom loglevel of the file handler
        logzero.loglevel(logging.INFO)
        logzero.logger.info("info2")
        logzero.logger.warn("warn2")

        with open(temp.name) as f:
            content = f.read()
            assert "] info1" not in content
            assert "] warn1" in content
            assert "] info2" not in content
            assert "] warn2" in content

    finally:
        temp.close()
