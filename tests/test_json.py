"""
test json related things
"""
import json
import tempfile
import logzero


def _test_json_obj_content(obj):
    # Check that all fields are contained
    attrs = ['asctime', 'filename', 'funcName', 'levelname', 'levelno', 'lineno', 'module', 'message', 'name', 'pathname', 'process', 'processName', 'threadName']
    assert obj["message"] == "info"
    for attr in attrs:
        if attr not in obj:
            raise Exception("obj missing key '%s'" % attr)


def test_json(capsys):
    """
    Test json logging
    """
    # Test setup_logger
    logger = logzero.setup_logger(json=True)
    logger.info('info')
    out, err = capsys.readouterr()
    _test_json_obj_content(json.loads(err))


def test_json_default_logger(capsys):
    # Test default logger
    logzero.reset_default_logger()
    logzero.logger.info('info')
    out, err = capsys.readouterr()
    assert "] info" in err

    logzero.json()
    logzero.logger.info('info')
    out, err = capsys.readouterr()
    _test_json_obj_content(json.loads(err))

    logzero.json(False)
    logzero.logger.info('info')
    out, err = capsys.readouterr()
    assert "] info" in err


def test_json_logfile(capsys):
    # Test default logger
    logzero.reset_default_logger()
    temp = tempfile.NamedTemporaryFile()
    try:
        logger = logzero.setup_logger(logfile=temp.name, json=True)
        logger.info('info')

        with open(temp.name) as f:
            content = f.read()
            _test_json_obj_content(json.loads(content))

    finally:
        temp.close()
