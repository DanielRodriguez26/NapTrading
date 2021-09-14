import modules.globalvariables as gb
from flask import request
import logging

#Variables globales
__globalvariables = gb.GlobalVariables()
__loggerIpClient = None

def getIPClient():

    __loggerIpClient = logging.getLogger('NAPIPClient')
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: %(message)s')
    handler = logging.FileHandler('NAP_Error_IPClient.log')
    handler.setLevel(logging.ERROR)
    handler.setFormatter(formatter)
    __loggerIpClient.addHandler(handler)

    hostClientIp = ''

    try:
        hostClientIp = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    except Exception as error:
        __loggerIpClient.exception(error)

    __loggerIpClient.removeHandler(handler)

    return hostClientIp
