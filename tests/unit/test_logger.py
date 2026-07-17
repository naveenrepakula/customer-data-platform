import logging

from src.common.logger import get_logger


def test_get_logger_disables_propagation():
    logger_name = "test_logger_disables_propagation"
    logger = logging.getLogger(logger_name)

    logger.handlers.clear()
    logger.propagate = True

    configured_logger = get_logger(logger_name)

    assert configured_logger.propagate is False

    configured_logger.handlers.clear()
