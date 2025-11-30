import logging

class NoStaticFilter(logging.Filter):
    def filter(self, record):
        return "/static/" not in record.getMessage()

accesslog = "-"
errorlog = "-"
loglevel = "info"

def post_fork(server, worker):
    logger = logging.getLogger("gunicorn.access")
    logger.addFilter(NoStaticFilter())
