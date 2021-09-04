import logging

class LoggerNotifyUser():
    def __init__(self):
        self.logger = logging.getLogger('NapTradingNotifyUser')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: %(message)s')
        handler = logging.FileHandler('naptrading_error_notifyuser.log')
        handler.setLevel(logging.ERROR)
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

        
    def exception(self, err):
        self.logger.exception(err)