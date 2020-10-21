"""
test json related things
"""
import json
import logzero


def _test_json_obj_content(obj):
    # Check that all fields are contained
    attrs = ['asctime', 'filename', 'funcName', 'levelname', 'levelno', 'lineno', 'module', 'message', 'name', 'pathname', 'process', 'processName', 'threadName']
    assert obj["message"] == "info"
    for attr in attrs:
        if attr not in obj:
            raise Exception(f"obj missing key '{attr}'")


def test_json(capsys):
    """
    Test json logging
    """
    # Test setup_logger
    logger = logzero.setup_logger(json=True)
    logger.info('info')
    out, err = capsys.readouterr()
    _test_json_obj_content(json.loads(err))


def test_json2(capsys):
    # Test default logger
    logzero.reset_default_logger()
    logzero.logger.info('info')
    out, err = capsys.readouterr()
    assert "] info" in err

    logzero.json()
    logzero.logger.info('info')
    out, err = capsys.readouterr()
    _test_json_obj_content(json.loads(err))

    # logzero.reset_default_logger()
    # # logzero.reset_default_logger('xx')
    # # logger = logzero.setup_logger()
    # # logger.info("test log output")
    # logzero.logger.info('test log output')

    # _out, err = capsys.readouterr()
    # assert "test log output" in err

# def test_myoutput(capsys):  # or use "capfd" for fd-level
#     import sys
#     print("hello")
#     sys.stderr.write("world\n")
#     captured = capsys.readouterr()
#     assert captured.out == "hello\n"
#     assert captured.err == "world\n"
#     print("next")
#     captured = capsys.readouterr()
#     assert captured.out == "next\n"

#     logzero.logger.info('info')
#     captured = capsys.readouterr()
#     assert "test_json:47" in captured.err
