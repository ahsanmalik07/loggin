import logging
from logging.handlers import RotatingFileHandler
from logging import Formatter
from colorlog import ColoredFormatter
import os
import sys
# sys.tracebacklimit = 0

class LogWriter(object):
    ALL_LOGS_FILE_PATH = "../LOGS/"
    def __init__(self, log_file_name):
        if not os.path.exists(self.ALL_LOGS_FILE_PATH + str(log_file_name) + '_ALL_LOGS'):
            os.makedirs(self.ALL_LOGS_FILE_PATH + log_file_name + '_ALL_LOGS')
        if not os.path.exists(self.ALL_LOGS_FILE_PATH + str(log_file_name) + '_ALL_LOGS/ERROR'):
            os.makedirs(self.ALL_LOGS_FILE_PATH + log_file_name + '_ALL_LOGS/ERROR')

        writeLogger = logging.getLogger(__name__)

        handler = RotatingFileHandler(
            filename=self.ALL_LOGS_FILE_PATH + log_file_name + '_ALL_LOGS/' + str(log_file_name) + 'Logs.log',
            mode="a", maxBytes=5 * 1024 * 1024, backupCount=20, encoding='utf-8', delay=0)
        logFormat = "%(asctime)s - %(levelname)s - %(message)s"
        formatter = Formatter(logFormat)
        handler.setFormatter(formatter)
        handler.setLevel(logging.DEBUG)
        if (writeLogger.hasHandlers()):
            writeLogger.handlers.clear()

        writeLogger.addHandler(handler)

        handlerOut = logging.StreamHandler()
        logFormatOut = "%(log_color)s%(asctime)s - %(levelname)s - %(message)s"
        formatterOut = ColoredFormatter(logFormatOut)
        handlerOut.setFormatter(formatterOut)
        writeLogger.addHandler(handlerOut)
        # handlerError = TimedRotatingFileHandler(filename=LogWriter.ALL_LOGS_FILE_PATH+logFileName+'_ALL_LOGS/ERROR/'+str(logFileName)+'Logs.err', when='midnight', backupCount=20, encoding='utf-8', delay=False)
        handlerError = RotatingFileHandler(
            filename=self.ALL_LOGS_FILE_PATH + log_file_name + '_ALL_LOGS/ERROR/' + str(log_file_name) + 'Logs.err',
            mode="a", maxBytes=5 * 1024 * 1024, backupCount=20, encoding='utf-8', delay=0)
        handlerError.setFormatter(formatter)
        handlerError.setLevel(logging.WARNING)

        writeLogger.addHandler(handlerError)
        writeLogger.setLevel(logging.DEBUG)
        self.log = writeLogger
        self.logFileName = log_file_name


    def write(self,log_desc=None, log_type="INFO"):
        if self.log == None or self.log == "":
            return None
        if log_type != "INFO" and log_type != "DEBUG" and log_type != "WARNING" and log_type != "ERROR" and log_type != "SCRIPT_COMPLETED":
            return None
        if log_type == "WARNING" or log_type == "ERROR":
            if log_type == "ERROR":
                self.log.exception(log_desc)
            else:
                self.log.warning(log_desc)
        else:
            if log_type == "SCRIPT_COMPLETED":
                self.log.info(
                    "==================================== script completed ====================================\n\n\n\n\n\n\n\n")
            else:
                self.log.info(log_desc)