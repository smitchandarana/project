'''
Created on Apr 18, 2019

@author: GANESHRAM KANAKASABAI
'''

import time # importing time 
import requests
from project import ConfigUtil

'''
HTTPClientPublisher via HTTP requests communicates with the Ubidots cloud
'''

class HTTPClientPublisher(object):
    '''
    classdocs
    '''

    url = ''
    TOKEN = ''
    
    def __init__(self):
        '''
        Constructor
        '''
        self.config = ConfigUtil.ConfigUtil()
        self.baseURL = self.config.getProperty(self.config.configConst.UBIDOTS_CLOUD_SECTION, self.config.configConst.CLOUD_BASE_URL)
        self.TOKEN = self.config.getProperty(self.config.configConst.MQTT_CLOUD_SECTION, self.config.configConst.USER_NAME_TOKEN_KEY)
    '''
    publish function is used to post HTTP requests to the Ubidots cloud
    @param label : label indicates the topic
    @param payload : payload indicates the data
    '''
        
    def publish(self, label, payload):
        # Creates the headers for the HTTP requests
        self.url = self.baseURL + label
        headers = {"X-Auth-Token": self.TOKEN, "Content-Type": "application/json"}
    
        # HTTP requests are being made
        status = 400
        attempts = 0
        while status >= 400 and attempts <= 5:
            print("sending request")
            req = requests.post(url=self.url, headers=headers,data= payload )
            status = req.status_code
            print(req.status_code)
            attempts += 1
            time.sleep(1)
    
        # Processing of the result is done
        if status >= 400:
            print("[ERROR] Could not send data after 5 attempts, please check \
                your token credentials and internet connection")
            return False
    
        print("[INFO] request made properly, your device is updated")
        return True