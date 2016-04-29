import logging
import inspect
import pprint

ANSIcolor = "\033[1;%dm"
endcolor = "\033[0m"
BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(30, 38)

COLORS = {
    'WARNING': YELLOW,
    'SUCCESS': GREEN,
    'INFO': WHITE,
    'DEBUG': BLUE,
    'CRITICAL': MAGENTA,
    'ERROR': RED
}

SUCCESS = 25


class ColorFormatter(logging.Formatter):

    def format(self, record):
        message = super(ColorFormatter, self).format(record)
        if record.levelname == 'INFO':
            return message
        else:
            return ANSIcolor % COLORS[record.levelname] + message + endcolor


class ColorLogger(logging.Logger):

    def __init__(self, name):
        super(ColorLogger, self).__init__(name, logging.DEBUG)

        logging.addLevelName(SUCCESS, 'SUCCESS')
        console = logging.StreamHandler()
        formatter = ColorFormatter('%(message)s')
        console.setFormatter(formatter)
        self.addHandler(console)

    def success(self, msg, *args, **kwargs):
        if self.isEnabledFor(SUCCESS):
            self._log(SUCCESS, msg, args, **kwargs)


    def debugvar(self, var, *args, **kwargs):
        frame = inspect.currentframe()
        stack = inspect.getouterframes(frame)
        prevframe = stack[1][0]
        msg = pprint.pformat(prevframe.f_locals[var])
        self.debug('Variable: %s' % var)
        self.debug(msg, *args, **kwargs)



def get_color_log():
    logging.setLoggerClass(ColorLogger)
    return logging.getLogger('log')

def get_summary_log():
    logging.setLoggerClass(ColorLogger)
    return logging.getLogger('logsummary')


log = get_color_log()
logsummary = get_summary_log()

log.info('--- ColorLog Color settings')
log.info('--- info')
log.debug('--- debug')
log.success('--- success')
log.error('--- error')
log.warning('--- warning')
log.critical('--- critical')
