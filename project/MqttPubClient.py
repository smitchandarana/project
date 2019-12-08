'''
Created on Feb 23, 2019
MqttPubClientTestApp.py: Python application to publish message using MQTT protocol
@author: GANESHRAM KANAKASABAI
'''
from project import MqttClientConnector

UBIDOTS_VARIABLE_LABEL = "/TempSensor"

UBIDOTS_TOPIC_DEFAULT = "/v1.6/devices/"

QOS = 2

class MqttPubClient(object):
    
    connector = None
    def __init__(self):
        '''
        MQTT publisher constructor, initializes the MQTT client connector.
        MQTT connector instance is being created
        '''
        
        self.connector = MqttClientConnector.MqttClientConnector()  
    '''
    Function connect is used to connect to the MQTT broker
    '''
        
    def connect(self):
        self.connector.connect()
    '''
    Function disconnect is used to disconnect from the MQTT broker
    ''' 
        
    def disconnect(self):
        self.connector.disconnect()
    '''
    Function to publish to the MQTT broker
    @param label : label indicates the topic
    @param sJSONobj: sJSONobj indicates JSON object data
    '''   
         
    def publish(self,label,sJSONobj):
        self.connector.publishMessage(UBIDOTS_TOPIC_DEFAULT + label, sJSONobj, QOS)
