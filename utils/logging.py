import logging
from airflow.models import Variable

logging_client = None


def get_logging_client():
    global logging_client

    if logging_client is None:
        logging.info('Initialising logging_client')

        log_level = Variable.get('bif_logging_level', 'INFO')

        numeric_level = getattr(logging, log_level.upper())

        if not isinstance(numeric_level, int):
            raise ValueError('Invalid log level: %s' % log_level)
        logging.basicConfig()
        logging.getLogger().setLevel(numeric_level)
        logging_client = logging

    return logging_client
