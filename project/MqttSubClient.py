'''
Created on Feb 23, 2019
MqttSubClientTestApp.py: python application to receive message using MQTT protocol
@author: GANESHRAM KANAKASABAI
'''
from project import MqttClientConnector

UBIDOTS_DEVICE_LABEL = "warehouse/"
UBIDOTS_TOPIC_DEFAULT = "/v1.6/devices/"
QOS = 2

class MqttSubClient(object):
    
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
    Function connect is used to disconnect to the MQTT broker
    '''
        
    def disconnect(self):
        self.connector.disconnect()
    '''
    Function to publish to the MQTT broker
    @param topic : topic indicates the MQTT topic
    '''
           
    def subscribe(self,topic):
        self.connector.subscibetoTopic(UBIDOTS_TOPIC_DEFAULT + UBIDOTS_DEVICE_LABEL + topic[0], None , QOS)
        self.connector.subscibetoTopic(UBIDOTS_TOPIC_DEFAULT + UBIDOTS_DEVICE_LABEL + topic[1], None , QOS)
        self.connector.subscibetoTopic(UBIDOTS_TOPIC_DEFAULT + UBIDOTS_DEVICE_LABEL + topic[2], None , QOS)