import logging

class Logger:
    logger = logging.getLogger('')
    logger.setLevel(logging.DEBUG)

    @staticmethod
    def info(message, *args, **kwargs):
        tags = ''.join(list(map(lambda x: f'[{x}]', args)))
        logging.info(f"{tags} {message} {kwargs if len(kwargs) > 0 else ''}")
