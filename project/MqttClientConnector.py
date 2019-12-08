'''
Created on Feb 23, 2019
MqttClientConnector.py: python class for implementing MQTT protocol connector
@author: GANESHRAM KANAKASABAI
'''
import logging 
import paho.mqtt.client as mqttClient  # MQTT client
import ssl 
from project import ConfigUtil
from project import SensorData
from time import sleep
from datetime import datetime
from project import DataUtil


class MqttClientConnector(object):
    '''
    MqttClientConnector: python class for implementing MQTT protocol connector
    @var port: MQTT port number in integer
    @var brokerAddr: complete address of the host server in String
    @var brockerKeepAlive: to stay active in integer
    @var mqttClient: instance of MQTT client class
    @var config: instance of ConfigUtil class
    @var dataUtil: instance of DataUtil class

    '''
    port = None
    brokerAddr = ""
    brockerKeepAlive = None
    mqttClient = None
    config = None
    dataUtil = None

    def __init__(self):
        '''
        MqttClientConnector Constructor
        '''
        self.createLogger()  # log the console output 
        self.mqttClient = mqttClient.Client()
        self.config = ConfigUtil.ConfigUtil()
        self.config.loadConfig()
        self.brokerAddr = self.config.getProperty(self.config.configConst.MQTT_CLOUD_SECTION, self.config.configConst.CLOUD_MQTT_BROKER)
        self.port = int(self.config.getProperty(self.config.configConst.MQTT_CLOUD_SECTION, self.config.configConst.SECURE_PORT_KEY))
        self.brockerKeepAlive = int(self.config.getProperty(self.config.configConst.MQTT_CLOUD_SECTION, self.config.configConst.KEEP_ALIVE_KEY))
        self.dataUtil = DataUtil.DataUtil()
        self.sensoData = SensorData.SensorData()
        self.username = self.config.getProperty(self.config.configConst.MQTT_CLOUD_SECTION, self.config.configConst.USER_NAME_TOKEN_KEY)
        self.password = ""
        self.TLS_CERT_PATH = r"ubidots_cert.pem"
        
                
    def createLogger(self):
        '''
        Function to create logger and console handler
        '''
        # create logger
        self.logger = logging.getLogger('MQTTClientConnector')
        self.logger.setLevel(logging.DEBUG)
        
        # create console handler and set level to debug
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        
        # create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        # add formatter to ch
        ch.setFormatter(formatter)
        
        # add ch to logger
        self.logger.addHandler(ch)
    
    def connect(self, connectionCallback=None , msgCallback=None):
        '''
        Function to connect to the MQTT host server
        @param connectionCallback: connection call back function
        @param msgCallback: message call back function
        '''
        if(connectionCallback != None):
            self.mqttClient.on_connect = connectionCallback
        else:
            self.mqttClient.on_connect = self.onConnect
            
        if(msgCallback != None) :
            self.mqclient.on_disconnect = msgCallback
        else :
            self.mqttClient.on_disconnect = self.onMessage
            
        self.mqttClient.on_message = self.onMessage    
        
        self.mqttClient.loop_start()
        self.mqttClient.username_pw_set(self.username, password=self.password)
        self.logger.info("Connecting to broker " + self.brokerAddr)
        self.mqttClient.tls_set(ca_certs=self.TLS_CERT_PATH, certfile=None,
                            keyfile=None, cert_reqs=ssl.CERT_REQUIRED,
                            tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)
        self.mqttClient.tls_insecure_set(False)
        self.mqttClient.connect(self.brokerAddr, self.port, self.brockerKeepAlive)
        
    def disconnect(self):
        '''
        Function to disconnect from the MQTT host server
        '''
        self.mqttClient.loop_stop()
        self.logger.info("Disconneting the MQTT  broker connection ")
        self.mqttClient.disconnect()
        
    def onConnect(self , client , userData , flags , rc):
        '''
        Function called when the broker responds to our connection request.
        @param flags: flags is a dict that contains response flags from the broker:
        flags['session present'] - this flag is useful for clients that are
            using clean session set to 0 only. If a client with clean
            session=0, that reconnects to a broker that it has previously
            connected to, this flag indicates whether the broker still has the
            session information for the client. If 1, the session still exists.
        @param rc: The value of rc determines success or not:
                    0: Connection successful
                    1: Connection refused - incorrect protocol version
                    2: Connection refused - invalid client identifier
                    3: Connection refused - server unavailable
                    4: Connection refused - bad username or password
                    5: Connection refused - not authorised
                    6-255: Currently unused.
        '''
        print("On connect RC : " + rc)
        if rc == 0:
            self.logger.info("Connected OK returned Code: " + rc)
        else:
            self.logger.debug("Bad connection Returned Code: " + rc)
            
    def onMessage(self , client , userdata , msg):
        '''
        Function called when a message has been received on a topic that the client subscribes to.
        @param msg: MQTTMessage that describes all of the message parameters.
        '''
        rcvdJSON = msg.payload.decode("utf-8")
        self.logger.info("\nReceived Topic is " + msg.topic + " --> \n" + str(rcvdJSON))
        self.dataUtil.updateActuatorData(msg.topic,rcvdJSON)
        #rcvdSensorData = self.dataUtil.toSensorDataFromJson(rcvdJSON)
        #self.logger.info("\nReceived Sensor Data :\n" + str(rcvdSensorData))
        #rcvdSensorDatatoJSON = self.dataUtil.toJsonFromSensorData(rcvdSensorData)
        #self.logger.info("\nReceived Sensor Data to JSON :\n" + str(rcvdSensorDatatoJSON))
        
    def publishMessage(self , topic , msg , qos=2):
        '''
        Publish a message on a topic causing a message to be sent to the broker and subsequently from
        the broker to any clients subscribing to matching topics.

        @param topic: The topic that the message should be published on.
        @param msg: The actual message to send. If not given, or set to None a
        zero length message will be used. Passing an int or float will result
        in the payload being converted to a string representing that number. If
        you wish to send a true int/float, use struct.pack() to create the
        payload you require.
        @param qos: The quality of service level to use.
        '''
        if qos < 0 or qos > 2 :
            qos = 2
            
        self.logger.info("\nTopic : "+ str(topic) + "\nMessage :\n" + str(msg))
        self.mqttClient.publish(topic, msg, qos)
        
    def publishAndDisconnect(self , topic , msg, qos=2):
        '''
        Function to establish MQTT connection, publish and disconnect
        @param topic: topic of the MQTT message in string
        @param msg: message payload
        @param qos: The quality of service level to use
        '''
        self.logger.info("\nTopic :\n" + str(topic))
        self.connect()
        #while True :
        self.publishMessage(topic, msg, qos)
        self.disconnect()
        
    def subscibetoTopic(self , topic , connnectionCallback=None , qos=2):
        '''
        Function to subscribe the client to one or more topics
        @param topic: topic of the MQTT message in string
        @param connnectionCallback: call back function on subscribe/on message
        @param qos: The quality of service level to use
        '''
        
        self.logger.info('subscibetoTopic : ' + topic)
        if (connnectionCallback != None):
            self.mqttClient.on_subscribe(connnectionCallback)
            self.mqttClient.on_message(connnectionCallback)
        
        self.mqttClient.subscribe(topic , qos)

        
    def unsubscibefromTopic(self , topic , connnectionCallback=None):
        '''
        Function to unsubscribe the client from one or more topics.
        @param topic: A single string, or list of strings that are the subscription topics to unsubscribe from.
        @param connnectionCallback: call back function on unsubscribe event
        '''
        if (connnectionCallback != None):
            self.mqttClient.on_unsubscribe(connnectionCallback)
               
        self.mqttClient.unsubscribe(topic)
        
    def subscribeAndDisconnect(self , topic , connnectionCallback=None , qos=2):
        '''
        Function to establish MQTT connection, subscribe the client to one or more topics and disconnect
        @param topic: topic of the MQTT message in string
        @param connnectionCallback: call back function on unsubscribe event
        @param qos: The quality of service level to use
        '''
        self.logger.info("\nTopic :\n" + str(topic))
        self.connect()
        self.subscibetoTopic(topic, connnectionCallback , qos)
        self.disconnect()
