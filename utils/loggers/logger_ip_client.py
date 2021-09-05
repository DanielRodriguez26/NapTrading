import logging

class LoggerIpClient():
    def __init__(self):
        self.logger = logging.getLogger('NapTradingIPClient')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: %(message)s')
        handler = logging.FileHandler('naptrading_error_ipclient.log')
        handler.setLevel(logging.ERROR)
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        
    def exception(self, err):
        self.logger.exception(err)
